# Author      : Zuguang Liu
# Date        : 2019-03-28 22:30:00
# Python Ver  : 3.6
# Description : Second gen of read email module, added class lookup module, 
# Update	  : In progress, put away later before implementation of core functions

import imaplib
import re
import email
import datetime
import pandas
import logging

def find_class(code):
	df=pandas.read_csv('lookup_table.csv',header=None)
	codel=df[0].tolist()
	namel=df[1].tolist()
	try:
		i=codel.index(code)
		return namel[i]
	except ValueError:
		return code

def read_schedule(): #function that returns a list of email messages on new appointments
	# The meta-structure ensures 99 retries to connect gmail; after 99 retries 
	com_attempt=0
	while True:
		try: 
			M = imaplib.IMAP4_SSL('imap.gmail.com')
			M.login('zgliu2z2@gmail.com', '********') #Contact Liu for autorization to see the password
			M.select('Inbox')
			# result,data = M.search(None, '(UNSEEN SUBJECT "Learning Commons")') #Email being fetched automatically marked as read
			result,data = M.search(None, '(SUBJECT "Schedule Reminder")')  #In case I want to double check schedule

			ids = data[0] # data is a list.
			id_list = ids.split() # ids is a space separated string
			msgl=[]
			for email_id in id_list:
				result, data = M.fetch(email_id, '(RFC822)') # fetch the email body for the given ID
				raw_email = data[0][1] #where the data is at
				msgl.append(email.message_from_bytes(raw_email)) #append the list with converted data
			M.close()
			M.logout()
		except Exception as e:
			if com_attempt<100:
				com_attempt+=1
				continue
			else:
				logging.error('Connection error after 99 retries - %s',e)
				return []
		break

	if len(msgl)>1:
		logging.error('Schedule checker failed due to one emails found')

	for i in range(len(msgl)):
		print(msgl[i].get_payload()[0].get_payload()) #first item of payload is readable text; second item is HTML crap)

	apptl=[] #initialize apptl, a list of dictionaries that contains detail of appoitnments
	# 	appt=dict()
	# 	tempstr=msgl[i].get_payload()[0].get_payload() #first item of payload is readable text; second item is HTML crap
	# 	appt['name']=re.search('Dear (.*),',tempstr).group(1)
	# 	date=re.search('Date: (.*)\r\n',tempstr).group(1) #Tuesday, March 26, 2019
	# 	date=date.split(', ')[1]+' '+date.split(', ')[2] #March 26 2019
	# 	time=re.search('Time: (.*)\r\n',tempstr).group(1) #9:30 AM
	# 	appt['start']=datetime.datetime.strptime(date+' '+time,'%B %d %Y %I:%M %p')
	# 	durat=re.search('Duration: (.*)\r\n',tempstr).group(1) #0.5 hour(s)
	# 	durat=float(durat.split(' ')[0]) #0.5
	# 	appt['end']=appt['start']+datetime.timedelta(hours = durat)
	# 	topic=re.search('Topic: (.*) ',tempstr).group(1)
	# 	subj=re.search('[a-zA-Z]+', topic)[0]
	# 	course_code=topic[topic.find(subj):(topic.find(subj)+len(subj)+4)]
	# 	appt['course']=find_class(course_code)
	# 	apptl.append(appt)
	# logging.info('%i appointments found from gmail in this period',len(apptl))
	# return apptl



read_schedule()
