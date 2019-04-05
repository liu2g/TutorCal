from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file

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
	# The meta-structure ensures 99 retries to connect google api; after 99 retries throw error and just return nothing
	com_attempt=0
	while True:
		try:
			credentials = get_credentials()
			http = credentials.authorize(httplib2.Http())
			service = discovery.build('calendar', 'v3', http=http, cache_discovery=False)
		except Exception as e:
			if com_attempt < 100:
				com_attempt += 1
				continue
			else:
				logging.error('GOOGLE API (GET) FAILED AFTER 99 ATTEMPTS, ERROR FOLLOWS\n%s', e)
				return
		break


	# Refer to the Python quickstart on how to setup the environment:
	# https://developers.google.com/google-apps/calendar/quickstart/python
	# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
	# stored credentials.

	try:
		event = {
			'summary': appt['name']+' - '+appt['course'],
			'start': {
				'dateTime': appt['start'].strftime('%Y-%m-%dT%H:%M:%S'),
				'timeZone': 'GMT-4:00', #central america time zone -4
			},
			'end': {
				'dateTime': appt['end'].strftime('%Y-%m-%dT%H:%M:%S'),
				'timeZone': 'GMT-4:00', #central america time zone -4
			},
		}
	except Exception as e:
		logging.error('ERROR WHEN DUMPING TO GOOGLE EVENT CONFIG FOR FOLLOWING APPOINTMENT\n%s\nERROR FOLLOWS\n%s',
		              str(appt),e)

	# The meta-structure ensures 99 retries to connect google api; after 99 retries throw error and just return nothing
	com_attempt=0
	while True:
		try:
			event = service.events().insert(calendarId='primary', body=event).execute()
		except Exception as e:
			if com_attempt < 100:
				com_attempt += 1
				continue
			else:
				logging.error('GOOGLE API (POST) FAILED AFTER 99 ATTEMPTS, ERROR FOLLOWS\n%s', e)
				return
		break

	logging.info('Event created for [%s] for course [%s] from [%s] to [%s]',
	             appt['name'],
	             appt['course'],
	             appt['start'].strftime('%Y-%m-%d %H:%M:%S'),
	             appt['end'].strftime('%Y-%m-%d %H:%M:%S'))
	return

def make_events(apptl):
	logging.info('--------Creating Events--------')
	if not apptl: #apptl is empty list
		logging.info('No events to create in this period')
		return
	for appt in apptl:
		make_event(appt)
