# -*- coding: utf-8 -*-
# Copyright (c) 2022, mietrecht.ch and Contributors
# See license.txt
from __future__ import unicode_literals


class TestHeizgradtagzahlen():
	def setup(self):
		self.data1 = 'data1'
		self.data2 = 'data2'

	def test_data_not_equals(self):
		assert self.data1 != self.data2