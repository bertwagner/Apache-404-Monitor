import smtplib
import os
import subprocess

FROM = os.environ["apache_404_monitor_email_from"]
FROM_PASSWORD = os.environ["apache_404_monitor_password"]
TO = [os.environ["apache_404_monitor_email_to"]]

BLOCKLIST = []


def FilterUninteresting404s():

    list_of_404s = []

    with open("access.log") as f:
        for line in f:
            if "404" in line:
                list_of_404s.append(line)
    
    print(list_of_404s)

def SendEmail():
    SUBJECT = 'test subject!'
    TEXT = 'this is the body of hte message!'

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(FROM, FROM_PASSWORD)
    server.sendmail(FROM, TO, message)
    server.close()
    print('successfully sent the mail')


if __name__ == "__main__":
    FilterUninteresting404s()
    SendEmail()

    