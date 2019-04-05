from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file

import datetime
import logging

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def make_event(appt):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/google-apps/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    event = {
      'summary': appt['name']+' - '+appt['course'],
      'start': {
        'dateTime': appt['start'].strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'GMT-5:00', #central america time zone -5
      },
      'end': {
        'dateTime': appt['end'].strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'GMT-5:00', #central america time zone -5
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    logging.info('Event created for [%s] for course [%s] from [%s] to [%s]',
                 appt['name'],
                 appt['course'],
                 appt['start'].strftime('%Y-%m-%dT%H:%M:%S'),
                 appt['end'].strftime('%Y-%m-%dT%H:%M:%S'))
    return

def make_events(apptl):
    if not apptl: #apptl is empty list
        logging.info('No appointments found in this period')
        return
    for appt in apptl:
        make_event(appt)