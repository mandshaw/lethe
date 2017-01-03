import os
import csv
from datetime import datetime

lethe_dir = os.path.dirname(__file__)

class PersonNotFoundError(BaseException):
    pass

class Person(object):
    """
    Class to store details of each person
    """

    def __init__(self, name, email, dob):
        """
        Constructor to create a person obj
        :param name: Name
        :param email: Email
        :param dob: Date of birth in format DD/MM/YYYY
        """
        self.name = name
        self.email = email
        self.dob = dob

    @property
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, dob):
        self._dob = datetime.strptime(dob, '%d/%m/%Y').date()


class RollarDex(object):
    """
    Class to read in a csv file and Create a RollarDex of People
    """
    def __init__(self, rollardex_source=None):
        if rollardex_source is None:
            rollardex_source = os.path.join(lethe_dir, 'birthdays.csv')
        with open(rollardex_source) as rollardex_csv:
            rollardex_reader = csv.reader(rollardex_csv)
            self.contents = [Person(row[0], row[1], row[2]) for row in rollardex_reader]

    def flip(self):
        for content in self.contents:
            yield content

    def find(self, name):
        for content in self.contents:
            if content.name == name:
                return content
        raise PersonNotFoundError('Could not find {name} in RollarDex'.format(name))

    def get_all_except(self, name):
        for content in self.contents:
            if content.name == name:
                continue
            else:
                yield content
