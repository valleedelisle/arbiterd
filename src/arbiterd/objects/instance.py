# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import typing as ty
from dataclasses import dataclass

from arbiterd.common import libvirt


@dataclass
class Instance:
    """Class to model a nova instance"""

    name: ty.Optional[str] = None
    uuid: ty.Optional[str] = None  # TODO: define a uuid type for this.
    # libvirt_domain_name: ty.Optional[str] = None
    _domain: 'libvirt.virDomain' = None
    # TODO: expose this as a property and store the parsed xml
    _xml_str: ty.Optional[str] = None

    def __eq__(self, other: 'Instance') -> bool:
        if not isinstance(other, Instance):
            return False
        return self.uuid == other.uuid

    @property
    def xml_str(self) -> str:
        if self._xml_str is None:
            self._xml_str = self.domain.XMLDesc(0)
        return self._xml_str

    @property
    def domain(self) -> 'libvirt.virDomain':
        if self._domain is None:
            if self.uuid:
                self._domain = libvirt.libvirt_obj.get_domain_by_uuid(
                    self.uuid)
                self.name = self._domain.name()
            elif self.name:
                self._domain = libvirt.libvirt_obj.get_domain_by_name(
                    self.name)
                self.uuid = self._domain.UUIDString()
            else:
                raise ValueError(
                    f'domain lookup failed, name or uuid must be set: {self}')
        return self._domain

    @property
    def is_nova_instance(self) -> bool:
        return 'nova:instance' in self.xml_str

    @classmethod
    def from_domain(cls, domain) -> 'Instance':
        return Instance(
            name=domain.name(), uuid=domain.UUIDString(), _domain=domain)
