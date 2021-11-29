# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import typing as ty

import testtools

from arbiterd.common import cpu


class TestCPU(testtools.TestCase):

    def test_parse_cpu_spec(self):
        data = cpu.parse_cpu_spec('1-4')
        self.assertIsInstance(data, ty.Set)
        self.assertEqual(data, {1, 2, 3, 4})
