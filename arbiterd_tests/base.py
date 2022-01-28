# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0
import fixtures
import testtools

from arbiterd_tests import fixtures as at_fixtures


class ATTestCase(testtools.TestCase):
    USE_ETC_FIXTURE = True
    USE_SYS_FIXTURE = True
    USE_LOG_FIXTURE = True

    def setUp(self):
        super().setUp()
        self.etc_fixture = (
            self.useFixture(at_fixtures.ETCFileSystemFixture())
            if self.USE_ETC_FIXTURE else None
        )
        self.sys_fixture = (
            self.useFixture(at_fixtures.SYSFileSystemFixture())
            if self.USE_SYS_FIXTURE else None
        )
        self.log_fixture = (
            self.useFixture(fixtures.FakeLogger())
            if self.USE_LOG_FIXTURE else None
        )

    def replace_log_fixture(self, log_level):
        self.log_fixture = self.useFixture(
            fixtures.FakeLogger(level=log_level))
