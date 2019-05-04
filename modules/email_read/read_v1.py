# Author      : Zuguang Liu
# Date        : 2019-03-28 22:30:00
# Python Ver  : 3.6
# Description : First gen of reading email module

import imaplib
import re

M = imaplib.IMAP4_SSL('imap.gmail.com')
M.login('zgliu2z2@gmail.com', '********') #Contact Liu for autorization to see the password
stat,count=M.select('Inbox')
stat,data=M.fetch(count[0],'(UID BODY[TEXT])')
notif=data[0][1].decode("utf-8") 
M.close()
M.logout()

student=re.search('Dear (.*),',notif).group(1)
date=re.search('Date: (.*)\r\n',notif).group(1)[0:-6]
time=re.search('Time: (.*)\r\n',notif).group(1)
topic=re.search('Topic: (.*) ',notif).group(1)
sub=re.search('[a-zA-Z]+', topic)[0]
course=topic[topic.find(sub):(topic.find(sub)+len(sub)+4)]
print(student,date,time,course)
