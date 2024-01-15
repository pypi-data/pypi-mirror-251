#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.parser.parse.
"""
import anyconfig.parser as TT

from . import common


class TestCase(common.TestCase):
    kind = 'parse'
    pattern = '*.*'

    def test_parse(self):
        for data in self.each_data():
            self.assertEqual(
                TT.parse(data.inp, **data.opts),
                data.exp,
                data
            )

# vim:sw=4:ts=4:et:
