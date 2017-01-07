import os
import sys
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
import logging


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
LOG.addHandler(ch)

def send_basic_email(recipients, birthday_boy_or_girl, weeks_away):
    # Create a text/plain message
    msg = MIMEText( "{name}'s {birthday} birthday is {num_weeks} weeks away on the {dob}".format(
        num_weeks=weeks_away,
        birthday=calculate_birthday(birthday_boy_or_girl),
        name=birthday_boy_or_girl.name,
        dob=birthday_boy_or_girl.dob.strftime("%d/%m/%Y")))

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = "Birthday Reminder for {name}".format(name=birthday_boy_or_girl.name)
    msg['From'] = "birthdayreminder@birthdayboy.com"

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP(os.environ.get('SMTP_HOST'), port=os.environ.get('SMTP_PORT'))
    s.login(user=os.environ.get('SMTP_USER'), password=os.environ.get('SMTP_PASSWORD'))
    s.sendmail("birthdayreminder@birthdayboy.com", [person.email for person in recipients], msg.as_string())
    LOG.info("Sending email to {people} for {bday}'s birtdhay".format(people=[person.name for person in recipients],bday=birthday_boy_or_girl.name))
    s.quit()

def calculate_birthday(person):
    today = datetime.today().date()
    birthday = today.year - person.dob.year
    if str(birthday).endswith('1'):
        return str(birthday) + 'st'
    elif str(birthday).endswith('2'):
        return str(birthday) + 'nd'
    elif str(birthday).endswith('3'):
        return str(birthday) + 'rd'
    else:
        return str(birthday) + 'th'