# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from rollardex import RollarDex
from email_utils import send_basic_email
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
ch = logging.StreamHandler()
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
            target_date = today + timedelta(days=28)
            if target_date.day == person.dob.day and target_date.month == person.dob.month:
                LOG.info('Birthday Coming up for {name}'.format(name=person.name))
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