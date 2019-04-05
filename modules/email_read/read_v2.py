# Author      : Zuguang Liu
# Date        : 2019-03-28 22:30:00
# Python Ver  : 3.6
# Description : Second gen of read email module

import imaplib
import re
import email

M = imaplib.IMAP4_SSL('imap.gmail.com')
M.login('zgliu2z2@gmail.com', 'zhong2bing')
M.select('Inbox')
# result,data = M.search(None, '(UNSEEN SUBJECT "Learning Commons")') #Email being fetched automatically marked as read
result,data = M.search(None, '(SUBJECT "Learning Commons")')
# result,data = M.search(None, '(UNSEEN SUBJECT "Schedule Reminder")')  #In case I want to double check schedule

ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
msgl=[]
for email_id in id_list:
	result, data = M.fetch(email_id, '(RFC822)') # fetch the email body for the given ID
	raw_email = data[0][1] #where the data is at
	msgl.append(email.message_from_bytes(raw_email)) #append the list with converted data
M.close()
M.logout()

for msg in msgl:
	print('************************************************************************************')
	print(msg.get_payload()[0].get_payload()) #first item is readable text; second item is HTML crap



# student=re.search('Dear (.*),',notif).group(1)
# date=re.search('Date: (.*)\r\n',notif).group(1)[0:-6]
# time=re.search('Time: (.*)\r\n',notif).group(1)
# topic=re.search('Topic: (.*) ',notif).group(1)
# sub=re.search('[a-zA-Z]+', topic)[0]
# course=topic[topic.find(sub):(topic.find(sub)+len(sub)+4)]
# print(student,date,time,course)