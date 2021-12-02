# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import os
from pprint import PrettyPrinter

from arbiterd.common import cpu, libvirt, nova
from arbiterd.objects import instance

LOG = logging.getLogger(__name__)
PRINTER = PrettyPrinter()
pprint = PRINTER.pprint
pformat = PRINTER.pformat

# TODO: decide on output convention.
# currently normal out is reported with pprint but
# errors, warnings and debug info will be logged.
# The default logging config logs at warn level and above.
# The default handler of last resort writes to sys.stderr


def list_command(args):

    if args.available_cpus:
        pprint(f'Available CPUs: {cpu.get_available_cpus()}')
    elif args.online_cpus:
        pprint(f'Online CPUs: {cpu.get_online_cpus()}')
    elif args.offline_cpus:
        pprint(f'Offline CPUs: {cpu.get_offline_cpus()}')
    elif args.dedicated_cpus:
        pprint(f'Dedicated CPUs: {nova.get_dedicated_cpus(args.nova_config)}')
    elif args.shared_cpus:
        pprint(f'Shared CPUs: {nova.get_shared_cpus(args.nova_config)}')
    elif args.domains:
        libvirt.init_libvirt()
        domains = [
            (dom.name(), dom.UUIDString())
            for dom in libvirt.libvirt_obj.list_domains()
        ]
        pprint(f'Libvirt Domains: {domains}')
    elif args.nova_domains:
        libvirt.init_libvirt()
        instances = []
        for dom in libvirt.libvirt_obj.list_domains():
            inst = instance.Instance.from_domain(dom)
            if inst.is_nova_instance:
                instances.append((inst.name, inst.uuid))
        pprint(f'Libvirt Domains: {instances}')
    else:
        # TBD: add support for listing  vcpu_pin_set from nova.conf.
        # TODO: add summary view.
        # TODO: add support for displaying pinned cpus currenly in used by
        # VMs on the host.
        # TODO: add support for listing kernel and userspace isolated cpus
        LOG.error(pformat(f'list was called with unsupported agrs: {args}'))
        fail(args)


def show_command(args):
    try:
        if args.domain_by_name:
            libvirt.init_libvirt()
            obj = instance.Instance(name=args.domain_by_name)
            print(f'Libvirt Domains:\n{obj.xml_str}')
        elif args.domain_by_uuid:
            libvirt.init_libvirt()
            obj = instance.Instance(uuid=args.domain_by_uuid)
            print(f'Libvirt Domains:\n{obj.xml_str}')
        elif args.cpu_state is not None:
            path = cpu.gen_cpu_path(args.cpu_state)
            online = cpu.get_online(path)
            print('ONLINE' if online else 'OFFLINE')
        else:
            LOG.error(
                pformat(f'show was called with unsupported agrs: {args}'))
            fail(args)
    except ValueError as e:
        LOG.error(e)
        fail(args)


def set_command(args):
    try:
        if args.cpu_online is not None:
            path = cpu.gen_cpu_path(args.cpu_online)
            if not cpu.set_online(path):
                fail(args)
        elif args.cpu_offline is not None:
            path = cpu.gen_cpu_path(args.cpu_offline)
            if not cpu.set_offline(path):
                fail(args)
        else:
            LOG.error(
                pformat(f'show was called with unsupported agrs: {args}'))
    except ValueError as e:
        LOG.error(e)
        fail(args)


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


def fail(args, code=1):
    LOG.debug(f'Command Failed {args}')
    exit(code)


def run():

    parser = argparse.ArgumentParser(description='Static CPU Arbiter')

    parser.add_argument(
        '--nova-config', dest='nova_config',
        default='/etc/nova/nova.conf', help='Path to nova config.')
    parser.add_argument(
        '--no-config', dest='no_config', action='store_true', default=False,
        help='skip config loading')
    parser.add_argument(
        '--debug', dest='debug', action='store_true', default=False,
        help='enable debug_logging')

    sub_commands = parser.add_subparsers()

    list_parser = sub_commands.add_parser('list')
    list_group = list_parser.add_mutually_exclusive_group(required=True)
    list_group.add_argument('--available-cpus', action='store_true')
    list_group.add_argument('--online-cpus', action='store_true')
    list_group.add_argument('--offline-cpus', action='store_true')
    list_group.add_argument('--dedicated-cpus', action='store_true')
    list_group.add_argument('--shared-cpus', action='store_true')
    list_group.add_argument('--domains', action='store_true')
    list_group.add_argument('--nova-domains', action='store_true')
    list_parser.set_defaults(func=list_command)

    show_parser = sub_commands.add_parser('show')
    show_group = show_parser.add_mutually_exclusive_group(required=True)
    show_group.add_argument(
        '--domain-by-name', type=str, help='The libvirt instance name')
    show_group.add_argument(
        '--domain-by-uuid', type=str, help='The libvirt instance uuid')
    show_group.add_argument(
        '--cpu-state', type=int, help='The online state of  cpu #',
        default=None
    )
    show_parser.set_defaults(func=show_command)

    set_parser = sub_commands.add_parser('set')
    set_group = set_parser.add_mutually_exclusive_group(required=True)
    set_group.add_argument(
        '--cpu-online', type=int, help='The online state of  cpu #',
        default=None
    )
    set_group.add_argument(
        '--cpu-offline', type=int, help='The online state of  cpu #',
        default=None
    )
    set_parser.set_defaults(func=set_command)

    args = parser.parse_args()
    # TODO: support external log config.
    if args.debug:
        logging.basicConfig(
            format=(
                '%(asctime)s,%(msecs)d %(levelname)-8s '
                '[%(filename)s:%(lineno)d] %(message)s'
            ),
            datefmt='%Y-%m-%d:%H:%M:%S', level=logging.DEBUG)
    if not args.no_config and not validate_gobal_configs(args):
        return
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()
