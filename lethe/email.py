import sendgrid
import os
from sendgrid.helpers.mail import *

def send_email(recipients, birthday_boy_or_girl):
    """
    Sends an email using send grid
    :param recipients: list of recipients
    :param birthday_boy_or_girl: Person who's email it is
    :return:
    """
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    email = build_email(recipients, birthday_boy_or_girl)
    response = sg.client.mail.send.post(request_body=email)


def build_email(recipients, birthday_boy_or_girl):
    mail = Mail()
    mail.set_from(Email("birthdayreminder@birthdayboy.com", "Birthday Reminder"))
    mail.set_subject("Birthday Reminder for {name}".format(name=birthday_boy_or_girl.name))

    personalization = Personalization()

    for recipient in recipients:
        personalization.add_to(Email(recipient.email, recipient.name))

    mail.add_personalization(personalization)

    mail.add_content(Content("text/plain", "{name}'s birthday is 4 weeks away on the {dob}".format(
        name=birthday_boy_or_girl.name,
        dob=birthday_boy_or_girl.dob.strftime("%d/%m/%Y"))))
    mail.add_content(Content("text/html", "<html><body>{name}'s birthday is 4 weeks away on the {dob}</body></html>".format(
        name=birthday_boy_or_girl.name,
        dob=birthday_boy_or_girl.dob.strftime("%d/%m/%Y"))))

    return mail.get()