# lethe
[![Build Status](https://travis-ci.org/mandshaw/lethe.svg?branch=master)](https://travis-ci.org/mandshaw/lethe)

Birthday reminder for those who suffer from forgetfulness 

## Description
lethe is a python library to send emails to a group of people when a person in their groups birthday is coming up. It takes a csv in the format below

```
Joe Blogs,joe.blogs@example.com,01/01/1970
```

If you place a file called _birthdays.csv_ in the lethe module it will pull it in when it runs

lethe uses SMTP to send emails and will require the following environment variables to be set

```
SMTP_HOST=your.smtp.host.here
SMTP_PORT=your.smptp.port.here
SMTP_USER=your.smtp.user.here
SMTP_PASSWORD=your.smtp.password.here
```
