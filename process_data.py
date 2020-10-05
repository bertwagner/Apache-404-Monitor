import smtplib
import os
import subprocess
import re
import json
import pandas as pd
import numpy as np

FROM = os.environ["apache_404_monitor_email_from"]
FROM_PASSWORD = os.environ["apache_404_monitor_password"]
TO = [os.environ["apache_404_monitor_email_to"]]

class ApachLogEntry(object):
    def __init__(self, raw_entry):
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?"(GET|POST|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH)(.*?)" (\d{3}) (\d{1,10}) "(.*?)" "(.*?)"',raw_entry)
        self.ip = match.group(1)
        self.verb = match.group(2)
        self.url = match.group(3)
        self.status_code = match.group(4)
        self.size = match.group(5)
        self.referrer = match.group(6)
        self.user_agent = match.group(7)
        self.raw = raw_entry
    
    def to_dict(self):
        return {
            'ip':self.ip,
            'verb':self.verb,
            'url':self.url,
            'status_code':self.status_code,
            'size':self.size,
            'referrer':self.referrer,
            'user_agent':self.user_agent,
            'raw':self.raw
        }

def ReadInExclusionList():
    try:
        exclusion_list = pd.read_pickle("exclusion_list.pkl")
        return exclusion_list
    except Exception as e:
        return pd.DataFrame()

def FilterNew404s(exclusion_list):

    parsed_entries = []

    with open("access.log") as f:
        for line in f:
            parsed_entries.append(ApachLogEntry(line))
            
    logs = pd.DataFrame.from_records([s.to_dict() for s in parsed_entries])
    
    logs_404s = logs[logs["status_code"] == "404"]

    try:
        # exclude entries already previously emailed
        new_logs_404s = logs_404s[~logs_404s.url.isin(exclusion_list.url)]
    except:
        new_logs_404s = logs_404s

    return new_logs_404s


def SendEmail(logs):
    SUBJECT = 'Daily BertWagner.com 404s'
    
    TEXT = ''
    
    for url in logs["url"].unique():
        TEXT += url + '\n'

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(FROM, FROM_PASSWORD)
    server.sendmail(FROM, TO, message)
    server.close()

def WriteToExclusionList(exclusion_list,new_entries):
    # We don't want these same URLs to appear in future reports, so we add them to the block list
    new_exclusion_list = pd.concat([exclusion_list,new_entries])
    new_exclusion_list.to_pickle("exclusion_list.pkl")

if __name__ == "__main__":
    exclusion_list = ReadInExclusionList()
    logs = FilterNew404s(exclusion_list)
    if len(logs.index) > 0:
        SendEmail(logs)
        WriteToExclusionList(exclusion_list,logs)

    