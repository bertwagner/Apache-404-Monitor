import smtplib
import os

def GetLog():
    pass

def FilterUninteresting404s():
    pass

def SendEmail():
    FROM = os.environ["apache_404_monitor_email_from"]
    TO = [os.environ["apache_404_monitor_email_to"]]
    SUBJECT = 'test subject!'
    TEXT = 'this is the body of hte message!'

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(FROM, os.environ["apache_404_monitor_password"])
    server.sendmail(FROM, TO, message)
    server.close()
    print('successfully sent the mail')


if __name__ == "__main__":
    
    # Need to set 3 environment variables before running
    # apache_404_monitor_email_from
    # apache_404_monitor_email_password
    # apache_404_monitor_email_to

    GetLog()
    FilterUninteresting404s()
    SendEmail()
    