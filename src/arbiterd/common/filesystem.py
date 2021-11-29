# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import os
import typing as ty

SYS = '/sys'
SYSFS = 'sysfs'
MTAB = '/etc/mtab'


def get_sys_fs_mount() -> str:
    """find the default sysfs mount point"""
    try:
        if os.path.exists(MTAB):
            with open(MTAB, mode='r') as mtab:
                mounts: ty.Set[str] = set()
                for line in mtab.readlines():
                    segments = line.split()
                    if segments[0] == SYSFS:
                        mounts.add(segments[1])
                    else:
                        return SYS
                return sorted(mounts, key=lambda path: len(path))[0]
    except OSError:
        # TODO: add logging
        pass
    return SYS

# derived from nova.virt.hardware
# https://github.com/openstack/nova/blob/8f250f5/nova/virt/hardware.py#L96-L155


def parse_cpu_spec(spec: str) -> ty.Set[int]:
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


def read_sys(
        path: str, sys: str = None, default: str = None
) -> ty.Optional[str]:
    sys = sys or get_sys_fs_mount()
    try:
        with open(os.path.join(sys, path), mode='r') as data:
            return data.read()
    except (OSError, ValueError):
        pass
    return default


def readlines_sys(path: str, sys: str = None) -> ty.List[str]:
    sys = sys or get_sys_fs_mount()
    try:
        with open(os.path.join(sys, path), mode='r') as data:
            return data.readlines()
    except (OSError, ValueError):
        pass
    return []

# TODO move to cpu module.


AVAILABLE_PATH = 'devices/system/cpu/present'


def get_available_cpus() -> ty.Set[int]:
    return parse_cpu_spec(read_sys(AVAILABLE_PATH)) or set()


ONLINE_PATH = 'devices/system/cpu/online'


def get_online_cpus() -> ty.Set[int]:
    return parse_cpu_spec(read_sys(ONLINE_PATH)) or set()


OFFLINE_PATH = 'devices/system/cpu/offline'


def get_offline_cpus() -> ty.Set[int]:
    return parse_cpu_spec(read_sys(OFFLINE_PATH)) or set()


def nproc() -> int:
    return len(get_available_cpus())


def gen_cpu_paths() -> ty.List[str]:
    sys = get_sys_fs_mount()
    for core in range(nproc()):
        yield str(os.path.join(sys, f'devices/system/cpu/cpu{core}'))


def get_online(cpu_path: str) -> bool:
    online = read_sys(os.path.join(cpu_path, 'online'), default='1').strip()
    return online == '1'
