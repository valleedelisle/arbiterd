# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
import tempfile
from unittest import mock

import fixtures

import arbiterd_tests.test_data as td

DATA_PATH_BASE = os.path.abspath(td.__path__[0])
SYS = 'sys'


class SYSFileSystemFixture(fixtures.Fixture):
    """Creates a fake /sys filesystem"""

    def _setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='arbiterd_tests')
        self.addCleanup(shutil.rmtree, self, 'temp_dir')
        self.sys_path = os.path.join(self.temp_dir, SYS)
        shutil.copytree(
            os.path.join(DATA_PATH_BASE, SYS),
            self.sys_path, symlinks=True,
            ignore_dangling_symlinks=True
        )
        sys_patcher = mock.patch(
            'arbiterd.common.filesystem.get_sys_fs_mount')
        self.sys_mock = sys_patcher.start()
        self.sys_mock.return_value = self.sys_path
        self.addCleanup(sys_patcher.stop)
