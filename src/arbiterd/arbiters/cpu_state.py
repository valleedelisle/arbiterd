# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import logging
from dataclasses import dataclass

from arbiterd.common import cpu
from arbiterd.objects import hardware_thread

LOG = logging.getLogger(__name__)


@dataclass
class CPUStateArbiter:
    TYPE: str = 'cpu-state'

    def arbitrate(self, context) -> str:
        vm_cores = {
            core for instance in context.instances
            for field in instance.cpu_affinities for core in field}
        managed_cores = {
            hw_thread.ident for hw_thread in context.managed_hardware_threads
        }
        unused_cores = managed_cores - vm_cores
        offlinable_cores = cpu.get_online_cpus() & managed_cores & unused_cores
        if context.dry_run:
            return f'offlinable_cpus: {offlinable_cores}'

        for core in offlinable_cores:
            logging.debug(
                f'offlining core: {core} as part of cpu_state arbitration')
            hardware_thread.HardwareThread(ident=core).online = False

        return f'offlined cpus: {offlinable_cores}'

    def revoke(self, context) -> str:
        if context.dry_run:
            return f'onlinable_cpus: {cpu.get_offline_cpus()}'
        for core in cpu.get_offline_cpus():
            logging.debug(f'onlining core: {core} as part of cpu_state revoke')
            hardware_thread.HardwareThread(ident=core).online = True
        return 'onlined: {cpu.get_offline_cpus()}'


def register(current_arbiters: dict) -> None:
    logging.debug(f'registering {CPUStateArbiter.TYPE} arbiter')
    current_arbiters[CPUStateArbiter.TYPE] = CPUStateArbiter
