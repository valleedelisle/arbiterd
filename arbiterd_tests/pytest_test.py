# -*- coding: utf-8 -*-
# Copyright 2021 - 2021, Sean Mooney and the arbiterd contributors
# SPDX-License-Identifier: Apache-2.0


import unittest


class TestPytest(unittest.TestCase):

    def test_framework_is_working(self):
        self.assertTrue(True)

    def test_import_worked(self):
        import arbiterd
        self.assertIsNotNone(arbiterd)
