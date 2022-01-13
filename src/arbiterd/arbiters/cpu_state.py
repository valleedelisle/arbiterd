# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0
import logging

import typeing as ty
from arbiterd.arbiters import base
from arbiterd.objects import context as ctx
from arbiterd.objects import hardware_thread


LOG = logging.getLogger(__name__)


class CPUStateArbiter(base.ArbiterBase):
    TYPE: str = 'cpu-state'

    def arbitrate(self, context: ctx.Context) -> str:
        vm_cores = {
            core for instance in context.instances
            for field in instance.cpu_affinities for core in field}
        offlinable_cores = (
            self.get_online_cores(context.managed_hardware_threads) - vm_cores
        )

        if context.dry_run:
            return f'offlinable_cpus: {offlinable_cores}'

        for core in offlinable_cores:
            logging.debug(
                f'offlining core: {core} as part of cpu_state arbitration')
            hardware_thread.HardwareThread(ident=core).online = False

        return f'offlined cpus: {offlinable_cores}'

    def get_online_cores(
            self, managed_cores: ty.List[hardware_thread.HardwareThread]
    ) -> ty.Set[int]:
        return {core.ident for core in managed_cores if core.online}

    def get_offline_cores(
            self, managed_cores: ty.List[hardware_thread.HardwareThread]
    ) -> ty.Set[int]:
        return {core.ident for core in managed_cores if not core.online}

    def revoke(self, context: ctx.Context) -> str:
        onlinable_cores = self.get_offline_cores(
            context.managed_hardware_threads
        )

        if context.dry_run:
            return f'onlinable_cpus: {onlinable_cores}'
        for core in onlinable_cores:
            logging.debug(f'onlining core: {core} as part of cpu_state revoke')
            hardware_thread.HardwareThread(ident=core).online = True
        return 'onlined: {onlinable_cores}'


def register(current_arbiters: dict) -> None:
    logging.debug(f'registering {CPUStateArbiter.TYPE} arbiter')
    current_arbiters[CPUStateArbiter.TYPE] = CPUStateArbiter
