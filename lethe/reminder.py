# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from lethe.rollardex import RollarDex
from lethe.email_utils import send_basic_email
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
LOG.addHandler(ch)

class BirthdayReminder(object):
    """
    Creates a rollardex and checks who's birthday is coming up
    """
    def __init__(self, rollardex_source=None):
        LOG.info('Creating a RollarDex')
        if rollardex_source is None:
            self.rollardex = RollarDex()
        else:
            self.rollardex = RollarDex(rollardex_source=rollardex_source)

    def check_birthdays(self):
        LOG.info('Checking for upcoming birthdays')
        today = datetime.today().date()
        for person in self.rollardex.flip():
            four_weeks_out = today + timedelta(days=28)
            two_weeks_out = today + timedelta(days=14)
            if four_weeks_out.day == person.dob.day and four_weeks_out.month == person.dob.month:
                LOG.info('Birthday Coming up in 4 weeks for {name}'.format(name=person.name))
                return self.send_notification(person)
            elif two_weeks_out.day == person.dob.day and two_weeks_out.month == person.dob.month:
                LOG.info('Birthday Coming up in 2 weeks for {name}'.format(name=person.name))
                return self.send_notification(person)
        LOG.info('No Birthdays Coming up')


    def send_notification(self, birthday_boy_or_girl):
        people_to_notify = [person for person in self.rollardex.get_all_except(birthday_boy_or_girl.name)]
        # send_email(people_to_notify, birthday_boy_or_girl)
        send_basic_email(people_to_notify, birthday_boy_or_girl)


def run():
    birthdays = BirthdayReminder()
    birthdays.check_birthdays()

if __name__ == '__main__':
    run()