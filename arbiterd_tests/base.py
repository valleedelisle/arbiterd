# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0

import fixtures
import testtools

from arbiterd_tests import fixtures as at_fixtures


class ATTestCase(testtools.TestCase):

    def setUp(self):
        super().setUp()
        self.sys_fixture = self.useFixture(at_fixtures.SYSFileSystemFixture())
        self.log_fixture = self.useFixture(fixtures.FakeLogger())

    def replace_log_fixture(self, log_level):
        self.log_fixture = self.useFixture(
            fixtures.FakeLogger(level=log_level))
