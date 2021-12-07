#!/usr/bin/env bash

_XTRACE_DEBUG=$(set +o | grep xtrace)
if [[ "${DEBUG_TRACING:-False}" == "True" ]]; then
    set -o xtrace
fi

FULL_PATH=$(realpath "${BASH_SOURCE[0]}")
TOOLS_DIR=$(dirname ${FULL_PATH})
CONFIG_DIR=${COFIG_DIR:-"/etc/arbiterd"}
CONFIG_FILE=${CONFIG_FILE:-"${CONFIG_DIR}/arbiterd.conf"}
SERVICE_FILE="/etc/systemd/system/arbiterd.service"
REPO_ROOT="$(realpath ${TOOLS_DIR}/.. )"

. $TOOLS_DIR/functions-common


function get_value {
    crudini --get ${CONFIG_FILE} $@
}

function set_value {
    crudini --set ${CONFIG_FILE} $1 $2 "$3"
}

function del_value {
    crudini --del ${CONFIG_FILE} $@
}

function is_set {
    output=$(crudini --get ${CONFIG_FILE} $* &> /dev/null ) && [ -n "$(crudini --get ${CONFIG_FILE} $*)" ]; echo $?
}

function show_config {
    cat  ${CONFIG_FILE}
}

function get_config {
    echo  ${CONFIG_FILE}
}

function del_config {
    sudo rm -f ${CONFIG_FILE}
}

function is_redhat_family {
    [[ -e /etc/redhat-release ]] ; echo $?
}

function gen_config {
    del_config
    sudo mkdir -p -m 777 ${CONFIG_DIR}
    touch ${CONFIG_FILE}
    if  [[ $(is_redhat_family) == 0 ]]; then
        set_value build container_runtime ${container_runtime:-"podman"}
    else
        set_value build container_runtime ${container_runtime:-"docker"}
    fi
    set_value build container_name ${container_name:-"arbiterd"}
    set_value build container_tag ${container_tag:-"latest"}
}

function init {
    gen_config
}

function is_git_repo {
    # this can be more robust but this will work for now
    [[ -e "${REPO_ROOT}/.git" ]] ; echo $?
}

function setup_source {
    if  [[ $(is_git_repo) == 0 ]]; then
        return
    fi
     # TODO: make this work
    die 'use of this script outside of its git repo is not supported'
}

function install {
    setup_source
    init
}

function clean {
    del_config
    sudo rm -rf ${CONFIG_DIR}
}

function uninstall {
    clean
}

function build_wheel {
    tox -e clean,build
}

function build_container {
    runtime=${container_runtime:-$(get_value build container_runtime)}
    name=${container_name:-$(get_value build container_name)}
    tag=${container_tag:-$(get_value build container_tag)}
    pushd ${REPO_ROOT}
    build_wheel
    build_command="${runtime} build -t ${name}:${tag} ."
    ${build_command}
    popd
}

function usage {
    cat << "EOF"
arbiterd-ctl.sh: A tool to configure arbiterd.

This tool automates the building, packaging and installation
of arbiterd.
commands:
  - install:
    - TODO: installs arebiterd as a systemd service.
    - TODO: installs arbiterd-ctl.sh  binary.
    - TODO: generates arbiterd configuration file.
  - uninstall:
    - TODO: stops arebiterd service.
    - TODO: uninstalls arebiterd systemd service.
    - TODO: runs clean
  - init:
    - create arbiterd directories
    - generate arbiterd configuration files.
  - clean:
    - removes arbiterd config files and directories
  - setup_source:
    - TODO: clone arbiterd if script is not executing form git repo.
            if the script is curled to bash (curl ... | bash) then clone
            a full copy of there repo. if the script is already in a
            git repo do nothing.
  - build_container:
    - builds contaniner image using \${CONTAINER_RUNTIME}
    - supported container runtimes are podman and docker.
    - The current container build is based on python:3.8-alpine
    - The contienr is built using the wheel produced by build-wheel
      which is invoked automatically as part of this command.
  - build_wheel:
    - build python wheel for arbiterd using tox
  - build_rpm:
    - TODO: build rpm for arbiterd.
  - usage:
    - prints this message
options:
  - debuging:
    - To enable debuging export DEBUG_TRACING=True
  - install:
    - The varibles described below can be defined to customise
      installation of arbiterd.
      <variable>=<value> arbiterd-ctl.sh install
    - container_runtime: docker|podman
    - container_name: any docker/podman allowable name default(arbiterd)
    - container_tag: any docker/podman allowable tag default(latest)
EOF

}

if [ $# -ge  1 ]; then
    func=$1
    shift
else
    func="usage"
fi

#replace with switch later
eval "$func $@"


${_XTRACE_DEBUG}
