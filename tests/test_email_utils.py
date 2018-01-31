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
from mock import patch, MagicMock, call
from lethe.email_utils import send_basic_email, calculate_birthday
from freezegun import freeze_time

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

class TestEmailUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @freeze_time('05/01/2017')
    @patch('lethe.email_utils.smtplib.SMTP')
    def test_send_4_week_email(self, smtp_mock):
        smtp_mocked_instance = MagicMock()
        smtp_mock.return_value = smtp_mocked_instance
        person1 = MagicMock(email='eva@noneofyourbusiness.com', dob=datetime.strptime('05/07/1993', '%d/%m/%Y'))
        person1.name = 'Eva'
        person2 = MagicMock(email='bob@noneofyourbusiness.com', dob=datetime.strptime('05/02/1993', '%d/%m/%Y'))
        person2.name = 'Bob'
        person2.organiser = 'Eva'
        send_basic_email(person1, person2, 4)
        self.assertEqual(
            smtp_mocked_instance.sendmail.assert_has_calls([
                call('birthdayreminder@birthdayboy.com', [], 'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: Birthday Reminder for Bob\nFrom: birthdayreminder@birthdayboy.com\n\nBob\'s 24th birthday is 4 weeks away on the 05/02/1993. Eva is organising their present.')
            ]),
            None
        )

    @freeze_time('05/01/2017')
    @patch('lethe.email_utils.smtplib.SMTP')
    def test_send_2_week_email(self, smtp_mock):
        smtp_mocked_instance = MagicMock()
        smtp_mock.return_value = smtp_mocked_instance
        person1 = MagicMock(email='eva@noneofyourbusiness.com', dob=datetime.strptime('05/07/1993', '%d/%m/%Y'))
        person1.name = 'Eva'
        person2 = MagicMock(email='bob@noneofyourbusiness.com', dob=datetime.strptime('05/02/1993', '%d/%m/%Y'))
        person2.name = 'Bob'
        person2.organiser = 'Eva'
        send_basic_email(person1, person2, 2)
        self.assertEqual(
            smtp_mocked_instance.sendmail.assert_has_calls([
                call('birthdayreminder@birthdayboy.com', [],
                     'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: Birthday Reminder for Bob\nFrom: birthdayreminder@birthdayboy.com\n\nBob\'s 24th birthday is 2 weeks away on the 05/02/1993. Eva is organising their present.')
            ]),
            None
        )

    @freeze_time('05/01/2017')
    def test_calculate_birthday(self):
        expected = {
            '21st' : MagicMock(dob=datetime.strptime('05/07/1996', '%d/%m/%Y')),
            '22nd' : MagicMock(dob=datetime.strptime('05/07/1995', '%d/%m/%Y')),
            '23rd' : MagicMock(dob=datetime.strptime('05/07/1994', '%d/%m/%Y')),
            '24th' : MagicMock(dob=datetime.strptime('05/07/1993', '%d/%m/%Y')),
            '30th' : MagicMock(dob=datetime.strptime('05/07/1987', '%d/%m/%Y')),
        }
        for expected_result, mock in expected.items():
            birthday = calculate_birthday(mock)
            self.assertEqual(birthday, expected_result)