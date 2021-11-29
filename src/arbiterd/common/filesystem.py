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
