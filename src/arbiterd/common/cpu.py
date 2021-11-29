# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import configparser
import functools
import os
import typing as ty

from arbiterd.common import filesystem


def parse_cpu_spec(spec: str) -> ty.Set[int]:
    # derived from nova.virt.hardware
    # https://github.com/openstack/nova/blob/8f250f5/nova/virt/hardware.py#L96-L155
    """Parse a CPU set specification.
    Each element in the list is either a single CPU number, a range of
    CPU numbers, or a caret followed by a CPU number to be excluded
    from a previous range.
    :param spec: cpu set string eg "1-4,^3,6"
    :returns: a set of CPU indexes
    """
    cpuset_ids: ty.Set[int] = set()
    cpuset_reject_ids: ty.Set[int] = set()
    for rule in spec.split(','):
        rule = rule.strip()
        # Handle multi ','
        if len(rule) < 1:
            continue
        # Note the count limit in the .split() call
        range_parts = rule.split('-', 1)
        if len(range_parts) > 1:
            reject = False
            if range_parts[0] and range_parts[0][0] == '^':
                reject = True
                range_parts[0] = str(range_parts[0][1:])
            # So, this was a range; start by converting the parts to ints
            start, end = [int(p.strip()) for p in range_parts]
            # Make sure it's a valid range
            if start > end:
                raise ValueError(f'Invalid range expression: {rule}')
            # Add available CPU ids to set
            if not reject:
                cpuset_ids |= set(range(start, end + 1))
            else:
                cpuset_reject_ids |= set(range(start, end + 1))
        elif rule[0] == '^':
            # Not a range, the rule is an exclusion rule; convert to int
            cpuset_reject_ids.add(int(rule[1:].strip()))
        else:
            # OK, a single CPU to include; convert to int
            cpuset_ids.add(int(rule))
    # Use sets to handle the exclusion rules for us
    cpuset_ids -= cpuset_reject_ids
    return cpuset_ids


AVAILABLE_PATH = 'devices/system/cpu/present'


def get_available_cpus() -> ty.Set[int]:
    return parse_cpu_spec(filesystem.read_sys(AVAILABLE_PATH)) or set()


ONLINE_PATH = 'devices/system/cpu/online'


def get_online_cpus() -> ty.Set[int]:
    return parse_cpu_spec(filesystem.read_sys(ONLINE_PATH)) or set()


OFFLINE_PATH = 'devices/system/cpu/offline'


def get_offline_cpus() -> ty.Set[int]:
    return parse_cpu_spec(filesystem.read_sys(OFFLINE_PATH)) or set()


def nproc() -> int:
    return len(get_available_cpus())


def gen_cpu_path(core: int) -> str:
    sys = filesystem.get_sys_fs_mount()
    return str(os.path.join(sys, f'devices/system/cpu/cpu{core}'))


def gen_cpu_paths() -> ty.Iterable[str]:
    sys = filesystem.get_sys_fs_mount()
    for core in range(nproc()):
        yield str(os.path.join(sys, f'devices/system/cpu/cpu{core}'))


def get_online(cpu_path: str) -> bool:
    online = filesystem.read_sys(
        os.path.join(cpu_path, 'online'), default='1').strip()
    return online == '1'


# TODO move nova functions to nova.py
@functools.lru_cache
def parse_nova_conf(nova_conf: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser(interpolation=None)
    config.read(nova_conf)
    return config


def get_string(
        conf: configparser.ConfigParser, section, option, default=None,
        strip=True
) -> str:

    data = conf.get(section, option, fallback=default)
    if data is not None and strip:
        data = data.strip('"').strip('\'')
    return data


def get_dedicated_cpus(nova_conf: str) -> ty.Set[int]:
    nova = parse_nova_conf(nova_conf)
    data = get_string(nova, 'compute', 'cpu_dedicated_set')
    if data is None:
        return set()
    return parse_cpu_spec(data)


def get_shared_cpus(nova_conf: str) -> ty.Set[int]:
    nova = parse_nova_conf(nova_conf)
    data = get_string(nova, 'compute', 'cpu_shared_set')
    if data is None:
        return set()
    return parse_cpu_spec(data)
