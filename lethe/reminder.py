# -*- coding: utf-8 -*-
import sys
import random
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
                self.figure_out_person_responsible(person)
                return self.send_notification(person, 4)
            elif two_weeks_out.day == person.dob.day and two_weeks_out.month == person.dob.month:
                LOG.info('Birthday Coming up in 2 weeks for {name}'.format(name=person.name))
                return self.send_notification(person, 2)
        LOG.info('No Birthdays Coming up')

    def figure_out_person_responsible(self, birthday_boy):
        current_iteration = max([person.checksum for person in self.rollardex.flip()])
        bought_already = [person.organiser for person in self.rollardex.flip() if person.checksum == current_iteration]
        left_to_buy = [
            person.name for person in self.rollardex.flip()
            if person.name != birthday_boy.name and person not in bought_already
        ]
        organiser = random.choice(left_to_buy)
        self.rollardex.update(birthday_boy, organiser, current_iteration)



    def send_notification(self, birthday_boy_or_girl, weeks_away):
        people_to_notify = [person for person in self.rollardex.get_all_except(birthday_boy_or_girl.name)]
        # send_email(people_to_notify, birthday_boy_or_girl)
        send_basic_email(people_to_notify, birthday_boy_or_girl, weeks_away)


def run():
    birthdays = BirthdayReminder()
    birthdays.check_birthdays()

if __name__ == '__main__':
    run()