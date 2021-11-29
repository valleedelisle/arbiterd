# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
from pprint import PrettyPrinter

from arbiterd.common import cpu

LOG = logging.getLogger(__name__)
PRINTER = PrettyPrinter()
pprint = PRINTER.pprint
pformat = PRINTER.pformat


def list_command(args):

    if args.available_cpus:
        pprint(f'Available CPUs: {cpu.get_available_cpus()}')
    elif args.online_cpus:
        pprint(f'Online CPUs: {cpu.get_online_cpus()}')
    elif args.offline_cpus:
        pprint(f'Online CPUs: {cpu.get_online_cpus()}')
    else:
        # TODO: add support for listing  cpu_share_set, cpu_dedicated_set
        # and vcpu_pin_set from nova.conf.
        # TODO: add support for displaying pinned cpus currenly in used by
        # VMs on the host.
        # TODO: add support for listing kernel and userspace isolated cpus
        LOG.error(pformat(f'list was called with unsupported agrs: {args}'))


def run():

    parser = argparse.ArgumentParser(description='Static CPU Arbiter')

    parser.add_argument(
        '--nova-config', dest='nova_config',
        default='/etc/nova/nova.conf', help='Path to nova config.')
    sub_commands = parser.add_subparsers()

    list_parser = sub_commands.add_parser('list')
    list_group = list_parser.add_mutually_exclusive_group(required=True)
    list_group.add_argument('--available-cpus', action='store_true')
    list_group.add_argument('--online-cpus', action='store_true')
    list_group.add_argument('--offline-cpus', action='store_true')
    list_parser.set_defaults(func=list_command)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()
