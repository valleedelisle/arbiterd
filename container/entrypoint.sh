#!/bin/sh
case "$1" in
    /bin/sh)
        mode="shell";;
    "")
        mode="default";;
    *)
        mode="args";;
esac
if [ "$mode" == "shell" ]; then
    /bin/sh
else
    if [ "$mode" == "default" ]; then
        ARGS="arbitrate --cpu-state"
        if ! [ "${DRY_RUN:-false}" == "true" ]; then
            ARGS="${ARGS} --apply"
        fi
    else
        ARGS=$@
    fi
    sudo arbiterd-static --debug $ARGS
fi
