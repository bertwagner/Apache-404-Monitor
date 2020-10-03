import smtplib
import os
import subprocess

FROM = os.environ["apache_404_monitor_email_from"]
FROM_PASSWORD = os.environ["apache_404_monitor_password"]
TO = [os.environ["apache_404_monitor_email_to"]]

def GetLog():
    # Assumes SSH keys set for passwordless login
    output = subprocess.Popen('cmd /k "C:\\Windows\\System32\\OpenSSH\\ssh.exe bertwagner@bertwagner.com"', shell=True, stdout=subprocess.PIPE).stdout.read()
    print(output)

def FilterUninteresting404s():
    pass

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
    GetLog()
    #FilterUninteresting404s()
    #SendEmail()
    