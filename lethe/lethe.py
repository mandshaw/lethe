# -*- coding: utf-8 -*-
from datetime import datetime
from rollardex import RollarDex

class BirthdayReminder(object):
    """
    Creates a rollardex and checks who's birthday is coming up
    """
    def __init__(self):
        self.rollardex = RollarDex()

    def check_birthdays(self):
        today = datetime.today().date()
        for person in self.rollardex.flip():
            day_delta = today - person.dob
            if day_delta.days == 28:
                # 4 weeks to go. YEOW
                self.send_notification(person.name)


    def send_notification(self, birthday_boy_or_girl):
        people_to_notify = [person for person in self.rollardex.get_all_except(birthday_boy_or_girl.name)]
        for person in people_to_notify:
            # TODO: Send emails
            print person.email