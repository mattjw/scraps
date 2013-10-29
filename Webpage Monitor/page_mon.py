#!/usr/local/bin/python

# A simple script that tracks URLs for changes. The three properties that the
# script monitors are described below. 
#
# Phrase Checking:
# Checks whether a phrase appears on a particular page. Triggers a notification
# the first time the phrase is found.
# See the `track_phrases` 
# dict.
#
# Change Checking:
# Checks whether the content on an existing page has changed since the last time
# it was checked. Triggers a notification each time the page has changed.
# See the `track_changes` dict.
#
# Page Existence Checking:
# Checks whether the page at a particular URL exists or not. Triggers a
# notification when the page becomes available.
# See the `track_existence` dict.
#
# All notifications are collected and sent as a batch report by e-mail. The 
# script will continue monitoring until killed.
#
# Instructions for use:
# Create a config.py file and fill it with the required fields:
# USERNAME, PASSWORD, SMTP_HOST, SMTP_PORT, FROM_EMAIL_ADDR, TO_EMAIL_ADDR
#
# Edit the three `track_*` dictionaries below as necessary.
#
# Author: Matt J Williams
# Year: 2013

import re
import urllib2
import hashlib
import time
from datetime import datetime
import smtplib
from email.MIMEText import MIMEText

import config
# Required fields:
# USERNAME, PASSWORD, SMTP_HOST, 
# SMTP_PORT, FROM_EMAIL_ADDR, TO_EMAIL_ADDR

#
# 
# Params
#
track_phrases = {'https://play.google.com/store/devices':[r"Nexus\s+5"],
                 'http://googleblog.blogspot.com':[r"Nexus\s+5"],}
track_changes = {}
track_existence = {'https://play.google.com/store/devices/details?id=nexus_5_8gb':False,
                   'https://play.google.com/store/devices/details?id=nexus_5_16gb':False,
                   'https://play.google.com/store/devices/details?id=nexus_5_white_8gb':False,
                   'https://play.google.com/store/devices/details?id=nexus_5_white_16gb':False,
                   'https://play.google.com/store/devices/details?id=nexus_5_8gb_white':False,
                   'https://play.google.com/store/devices/details?id=nexus_5_16gb_white':False,}
WAIT_DUR = 30 # secs
SUBJECT_LINE = "! PAGE CHANGE DETECTED ! "
ADDR_TO = config.TO_EMAIL_ADDR

#
#
# Prep OS X notificaiton center (if pync is available)
#
try:
    from pync import Notifier
    do_osx_notifications = True
except ImportError:
    do_osx_notifications = False

#
#
# Monitoring
#
print "STARTING..."
num_repeats = 0
while True:

    #
    # Prep a change report
    # If `report` ends up being non-empty then we've got a notifiation to send
    report = ""
    try:
        #
        # Check for phrase
        for url, phrases in track_phrases.iteritems():
            culled = list(phrases)

            resp = urllib2.urlopen(url)
            html = resp.read()

            for phrase in phrases:
                m = re.search( phrase, html )
                if m is not None:
                    report += "[Phrase Matched] Phrase = %s; URL = %s \n" % (url, phrase) 
                    culled.remove( phrase )

            track_phrases[url] = culled

        #
        # Check for existing page changes (any change to HTML will trigger)
        for url, orig_digest in track_changes.iteritems():
            resp = urllib2.urlopen(url)
            page_html = resp.read()
            page_md5 = hashlib.md5(page_html).hexdigest()

            if orig_digest is None:
                track_changes[url] = page_md5
                continue

            if page_md5 != orig_digest:
                report += "[Page Changed] URL = %s\n" % url
                track_changes[url] = page_md5

        #
        # Check if a page has appeared
        for url, was_found in track_existence.iteritems():
            if was_found:
                continue
            try:
                resp = urllib2.urlopen(url)
                code = resp.getcode()
                if code == 200:
                    track_existence[url] = True
                    report += "[Page Appeared] URL = %s\n" % (url)
            except urllib2.URLError:
                continue

    except IOError, err:
        print "ERROR:", err

    #
    # Generate report (if necessary)
    # All changes detected in this run are sent as a batch
    if report:
        print "SENDING REPORT:"
        print report

        # E-mail
        mime_msg = MIMEText(report)
        mime_msg['Subject'] = SUBJECT_LINE
        mime_msg['From'] = config.SENDER_EMAIL_ADDR
        mime_msg['Reply-to'] = config.SENDER_EMAIL_ADDR
        mime_msg['To'] = ADDR_TO
        mime_msg['Cc'] = config.SENDER_EMAIL_ADDR
        msg = mime_msg.as_string()

        server = smtplib.SMTP_SSL(host=config.SMTP_HOST,port=config.SMTP_PORT)
        server.login(config.USERNAME, config.PASSWORD)

        server.sendmail( config.SENDER_EMAIL_ADDR, [ADDR_TO, config.SENDER_EMAIL_ADDR], msg )  # copies self
        server.quit()

        #
        # OS X notification
        if do_osx_notifications:
            Notifier.notify( "Page change detected" )

    #
    # Sleep...
    num_repeats += 1
    if not num_repeats % 60 or num_repeats <= 5:
        print '%s batch check so far. Last check at %s.' % (num_repeats, datetime.now())
    time.sleep( WAIT_DUR )


