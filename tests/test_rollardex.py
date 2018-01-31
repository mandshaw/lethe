#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lethe
----------------------------------

Tests for `lethe` module.
"""


import sys
import shutil
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
        person = Person('Eva', 'eva@noneofyourbusiness.com', '05/07/1993', '', '')
        self.assertEqual(person.name, 'Eva')
        self.assertEqual(person.email, 'eva@noneofyourbusiness.com')
        self.assertEqual(person.dob, datetime.strptime('05/07/1993','%d/%m/%Y').date())

    def test_rollar_dex(self):
        rollardex = RollarDex(rollardex_source=os.path.join(fixtures_dir, 'birthdays.csv'))
        people = [person for person in rollardex.flip()]
        self.assertEqual(len(people), 2)
        self.assertTrue(isinstance(people[0], Person))

    def test_rollar_dex_find(self):
        rollardex = RollarDex(rollardex_source=os.path.join(fixtures_dir, 'birthdays.csv'))
        jane = rollardex.find('Jane')
        self.assertTrue(isinstance(jane, Person))
        self.assertTrue(jane.name, 'Jane')

    def test_rollar_dex_get_all_except(self):
        rollardex = RollarDex(rollardex_source=os.path.join(fixtures_dir, 'birthdays.csv'))
        people = [person for person in rollardex.get_all_except('Jane')]
        self.assertEqual(len(people), 1)
        self.assertTrue(isinstance(people[0], Person))
        self.assertTrue(people[0].name, 'Bob')

    def test_rollar_dex_udpate(self):
        try:
            shutil.copyfile(os.path.join(fixtures_dir, 'birthdays.csv'), os.path.join(fixtures_dir, 'birthdays1.csv'))
            rollardex = RollarDex(rollardex_source=os.path.join(fixtures_dir, 'birthdays1.csv'))
            rollardex.update(rollardex.find('Jane'), 'Foo', 1)
            rollardex = RollarDex(rollardex_source=os.path.join(fixtures_dir, 'birthdays1.csv'))
            self.assertEqual(rollardex.find('Jane').organiser, 'Foo')
            self.assertEqual(rollardex.find('Jane').checksum, '1')
        finally:
            os.remove(os.path.join(fixtures_dir, 'birthdays1.csv'))
