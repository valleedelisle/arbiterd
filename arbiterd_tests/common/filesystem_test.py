# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import os
import typing as ty
from unittest import mock

import testtools
from testtools.content import text_content

from arbiterd.common import filesystem
from arbiterd_tests import base
from arbiterd_tests import fixtures as at_fixtures


class TestFSCommon(testtools.TestCase):

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


class TestFSTestData(testtools.TestCase):

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

    def test_sysfs_fixture(self):
        fs_fixture = at_fixtures.SYSFileSystemFixture()
        self.useFixture(fs_fixture)
        self.assertTrue(os.path.exists(fs_fixture.temp_dir))
        self.assertTrue(os.path.exists(fs_fixture.sys_path))
        self.assertIs(filesystem.get_sys_fs_mount, fs_fixture.sys_mock)
        self.assertEqual(fs_fixture.sys_path, filesystem.get_sys_fs_mount())

# This is a functional test class that use the sysfs test fixture
# to create a fake copy of /sys which it the used in the tests.


class TestCPUData(base.ATTestCase):

    # the sysfs test fixture has 48 cores
    def test_available_cpus(self):
        cpus = filesystem.get_available_cpus()
        self.assertEqual({x for x in range(48)}, cpus)
    # all cores are online

    def test_online_cpus(self):
        cpus = filesystem.get_online_cpus()
        self.assertEqual({x for x in range(48)}, cpus)
    # so the offline cpus should be empty

    def test_offline_cpus(self):
        cpus = filesystem.get_offline_cpus()
        self.assertEqual(set(), cpus)
    # the total amount of cpus should be the union of the online
    # and offline cpus.

    def test_available_equals_online_and_offline(self):
        self.assertEqual(
            filesystem.get_available_cpus(),
            {*filesystem.get_online_cpus(), *filesystem.get_offline_cpus()}
        )
    # the total number of cpus should be 48

    def test_nproc(self):
        self.assertEqual(filesystem.nproc(), 48)
    # the per cpu paths should exist within the sys mount

    def test_gen_cpu_paths(self):
        sys = filesystem.get_sys_fs_mount()
        expected = []
        for core in range(48):
            path = os.path.join(sys, f'devices/system/cpu/cpu{core}')
            self.assertTrue(os.path.exists(path))
            expected.append(str(path))
        self.assertEqual(list(filesystem.gen_cpu_paths()), expected)
    # and each cpu should report itself as online.

    def test_get_online(self):
        for cpu in filesystem.gen_cpu_paths():
            self.addDetail(
                f'cpu-online path={cpu}',
                text_content(
                    filesystem.read_sys(os.path.join(cpu, 'online')) or
                    'not present')
            )
            self.assertTrue(
                filesystem.get_online(cpu), f'cpu:{cpu} is offline')
