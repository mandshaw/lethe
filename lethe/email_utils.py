import os
import smtplib
from email.mime.text import MIMEText

def send_basic_email(recipients, birthday_boy_or_girl):
    # Create a text/plain message
    msg = MIMEText( "{name}'s birthday is 4 weeks away on the {dob}".format(
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
    s.quit()