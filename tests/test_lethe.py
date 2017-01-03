#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lethe
----------------------------------

Tests for `lethe` module.
"""


import sys
import unittest
from datetime import datetime
import os
from lethe.rollardex import Person, RollarDex

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

class TestRollarDex(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_person(self):
        person = Person('Eva', 'eva@noneofyourbusiness.com', '05/07/1993')
        self.assertEqual(person.name, 'Eva')
        self.assertEqual(person.email, 'eva@noneofyourbusiness.com')
        self.assertEqual(person.dob, datetime.strptime('05/07/1993','%d/%m/%Y').date())
