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
from mock import patch, MagicMock
from freezegun import freeze_time
from lethe.reminder import BirthdayReminder
from lethe.rollardex import Person

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

class TestRollarDex(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('lethe.reminder.BirthdayReminder.send_notification')
    def test_birthday_check_no_match(self, notification_mock):
        birthdays = BirthdayReminder(rollardex_source=os.path.join(fixtures_dir, 'birthdays.csv'))
        birthdays.check_birthdays()
        self.assertFalse(notification_mock.called)

    @freeze_time('2017-07-19')
    @patch('lethe.reminder.BirthdayReminder.send_notification')
    def test_birthday_check_birthday_found_four_weeks(self, notification_mock):
        birthdays = BirthdayReminder(rollardex_source=os.path.join(fixtures_dir, 'birthdays.csv'))
        birthdays.check_birthdays()
        self.assertTrue(notification_mock.called)
        self.assertEquals(notification_mock.call_args[0][0].name, 'Bob')

    @freeze_time('2017-08-02')
    @patch('lethe.reminder.BirthdayReminder.send_notification')
    def test_birthday_check_birthday_found_2_weeks(self, notification_mock):
        birthdays = BirthdayReminder(rollardex_source=os.path.join(fixtures_dir, 'birthdays.csv'))
        birthdays.check_birthdays()
        self.assertTrue(notification_mock.called)
        self.assertEquals(notification_mock.call_args[0][0].name, 'Bob')

    @patch('lethe.reminder.send_basic_email')
    def test_send_notification(self, send_email_mock):
        birthdays = BirthdayReminder(rollardex_source=os.path.join(fixtures_dir, 'birthdays.csv'))
        birthdays.send_notification(Person('Bob', 'test@test.com', '01/01/1999'), 2)
        self.assertEqual(len(send_email_mock.call_args[0][0]), 1)
        self.assertEqual(send_email_mock.call_args[0][0][0].name, 'Jane')
        self.assertEqual(send_email_mock.call_args[0][1].name, 'Bob')

