# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0


import os
import typing as ty
import unittest
from unittest import mock

from arbiterd.common import filesystem


class TestFSCommon(unittest.TestCase):

    def test_get_sys_fs_mount(self):
        mtab_data = 'sysfs /sys'
        open_mock = mock.mock_open(read_data=mtab_data)
        with mock.patch('builtins.open', open_mock) as m_open:
            self.assertEqual(filesystem.SYS, filesystem.get_sys_fs_mount())
            m_open.assert_called_once()

    def test_get_sys_fs_mount_raises(self):
        with mock.patch('builtins.open', side_effect=OSError()) as m_open:
            self.assertEqual(filesystem.SYS, filesystem.get_sys_fs_mount())
            m_open.assert_called_once()

    def test_get_sys_fs_mount_non_default_location(self):
        mtab_data = 'sysfs /sysfs'
        open_mock = mock.mock_open(read_data=mtab_data)
        with mock.patch('builtins.open', open_mock) as m_open:
            self.assertEqual('/sysfs', filesystem.get_sys_fs_mount())
            m_open.assert_called_once()

    def test_get_sys_fs_mount_shortest_mount_path(self):
        mtab_data = (b'sysfs /sys\n'
                     b'sysfs /sysfs')
        open_mock = mock.mock_open(read_data=mtab_data)
        with mock.patch('builtins.open', open_mock) as m_open:
            self.assertEqual(filesystem.SYS, filesystem.get_sys_fs_mount())
            m_open.assert_called_once()

    def test_parse_cpu_spec(self):
        data = filesystem.parse_cpu_spec('1-4')
        self.assertIsInstance(data, ty.Set)
        self.assertEqual(data, {1, 2, 3, 4})


class TestFSTestData(unittest.TestCase):

    def test_import_test_data(self):
        import arbiterd_tests.test_data as td
        self.assertIsNotNone(td)

    def test_sysfs_test_data_exists(self):
        import arbiterd_tests.test_data as td
        data_path_base = os.path.abspath(td.__path__[0])
        print(data_path_base)
        self.assertTrue(os.path.exists(data_path_base))
        sys_path = os.path.join(data_path_base, filesystem.SYS)
        self.assertTrue(os.path.exists(sys_path))
