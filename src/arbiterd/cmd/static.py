# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import os
from pprint import PrettyPrinter

from arbiterd.common import cpu, libvirt, nova

LOG = logging.getLogger(__name__)
PRINTER = PrettyPrinter()
pprint = PRINTER.pprint
pformat = PRINTER.pformat

# TODO: decide on output convention.
# currently normal out is reported with pprint but
# errors, warnings and debug info will be logged.
# The default logging config logs at warn level and above.
# The default handler of last resort writes to sys.stderr


libvirt_obj = None


def init_libvirt():
    global libvirt_obj
    if libvirt_obj is None:
        libvirt_obj = libvirt.Libvirt()


def list_command(args):

    if args.available_cpus:
        pprint(f'Available CPUs: {cpu.get_available_cpus()}')
    elif args.online_cpus:
        pprint(f'Online CPUs: {cpu.get_online_cpus()}')
    elif args.offline_cpus:
        pprint(f'Online CPUs: {cpu.get_online_cpus()}')
    elif args.dedicated_cpus:
        pprint(f'Dedicated CPUs: {nova.get_dedicated_cpus(args.nova_config)}')
    elif args.shared_cpus:
        pprint(f'Shared CPUs: {nova.get_shared_cpus(args.nova_config)}')
    elif args.domains:
        init_libvirt()
        domains = [
            (dom.name(), dom.UUIDString(),
             {idx: cpus for idx, cpus in enumerate(dom.vcpuPinInfo())})
            for dom in libvirt_obj.list_domains()
        ]
        pprint(f'Libvirt Domains: {domains}')
    else:
        # TBD: add support for listing  vcpu_pin_set from nova.conf.
        # TODO: add summary view.
        # TODO: add support for displaying pinned cpus currenly in used by
        # VMs on the host.
        # TODO: add support for listing kernel and userspace isolated cpus
        LOG.error(pformat(f'list was called with unsupported agrs: {args}'))


def validate_gobal_configs(args):
    result = os.path.exists(args.nova_config)
    if not result:
        err = pformat(
            'Config validation is enabled but the nova config file cannot '
            'be found at {args.nova_config}. Pass --no-config to disable '
            'validation or --nova-config <path> if it exits at a non default '
            'location.'
        )
        LOG.error(err)
    return result


def run():

    parser = argparse.ArgumentParser(description='Static CPU Arbiter')

    parser.add_argument(
        '--nova-config', dest='nova_config',
        default='/etc/nova/nova.conf', help='Path to nova config.')
    parser.add_argument(
        '--no-config', dest='no_config', action='store_true', default=False,
        help='skip config loading')

    sub_commands = parser.add_subparsers()

    list_parser = sub_commands.add_parser('list')
    list_group = list_parser.add_mutually_exclusive_group(required=True)
    list_group.add_argument('--available-cpus', action='store_true')
    list_group.add_argument('--online-cpus', action='store_true')
    list_group.add_argument('--offline-cpus', action='store_true')
    list_group.add_argument('--dedicated-cpus', action='store_true')
    list_group.add_argument('--shared-cpus', action='store_true')
    list_group.add_argument('--domains', action='store_true')
    list_parser.set_defaults(func=list_command)

    args = parser.parse_args()
    if not args.no_config and not validate_gobal_configs(args):
        return
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()
