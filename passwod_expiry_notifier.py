#!/usr/bin/env python
###############################################################################
# Pupose        :- Notify on Email befor password expires - Linux, unix, BSD etc
# Author        :- Muhammed Iqbal
# Created       :- 24-Jan-2018
# Version       :- 0.2
# License       :- free
###############################################################################

import datetime
import socket
import sys
import smtplib
import subprocess, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment

###############################################################################

reciever_name = "Full Name Of Reciever"
sender = 'name@domain.'
receiver = 'name@domain.'
company_logo = "http://url/Logo.png"
mailheader = "Password Expiry Notification"

###############################################################################

hostname = socket.gethostname()
today = datetime.datetime.today()
username = sys.argv[1]

###############################################################################

def expiry_check():
  global md
  with open( "/etc/shadow" ) as shadow:
       for aLine in shadow:
           filed = aLine.split(":")
           lu = filed[2]
           md = filed[4]
           ws = filed[5]
           try:
               if (filed[0] == username):
                  global warnstr
                  global lastupdate
                  global expiry
                  global remdays
                  lu = int(lu)
                  md = int(md)
                  ws = int(ws)
                  lastupdate = datetime.datetime.fromtimestamp(lu*60*60*24)
                  expiry = lastupdate + datetime.timedelta(md)
                  warnstr = (expiry - datetime.timedelta(ws))
                  remdays = (expiry - today)
           except ValueError:
                pasis


###############################################################################

def email():

    line = "This email is a gentle reminder for you to reset your account password which would expire in %s days! " % (remdays.days)
    #Compose Email
    TEMPLATE = open("Email.html","r").read()
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Linux User Password Expiry - %s' % username
    msgRoot['From'] = sender
    msgRoot['To'] = receiver

    body = MIMEText(
           Environment().from_string(TEMPLATE).render(
           header = emailheader,
           machine = hostname,
           username = username,
           logo = company_logo,
           date = expiry.date(),
           dear = reciever_name,
           data = line           
    ), 'html')
    msgRoot.attach(body)

    #SMTP
    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(sender, receiver, msgRoot.as_string())
       smtpObj.quit()
       print "Successfully sent email"
    except:
      print "There was an error sending the email. Check the smtp settings."

###############################################################################

def main():
    expiry_check()
    if today >= warnstr:
       email()
main()

