import smtplib
import os
import subprocess
import re
import json
import pandas as pd

FROM = os.environ["apache_404_monitor_email_from"]
FROM_PASSWORD = os.environ["apache_404_monitor_password"]
TO = [os.environ["apache_404_monitor_email_to"]]

BLOCKLIST = []


class ApachLogEntry(object):
    def __init__(self, raw_entry):
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?"([GET|POST|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH].*?)" (\d{3}) (\d{1,10}) "(.*?)" "(.*?)"',raw_entry)
        self.ip = match.group(1)
        self.request = match.group(2)
        self.status_code = match.group(3)
        self.size = match.group(4)
        self.referrer = match.group(5)
        self.user_agent = match.group(6)
        self.raw = raw_entry
    
    def to_dict(self):
        return {
            'ip':self.ip,
            'request':self.request,
            'status_code':self.status_code,
            'size':self.size,
            'referrer':self.referrer,
            'user_agent':self.user_agent,
            'raw':self.raw
        }

def FilterUninteresting404s():

    parsed_entries = []

    with open("access.log") as f:
        for line in f:
            parsed_entries.append(ApachLogEntry(line))
            
    df = pd.DataFrame.from_records([s.to_dict() for s in parsed_entries])
    test=5


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

def AddEntriesToBlockList():
    # We don't want these same URLs to appear in future reports, so we add them to the block list
    pass

if __name__ == "__main__":
    FilterUninteresting404s()
    #SendEmail()
    AddEntriesToBlockList()

    