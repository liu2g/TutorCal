# Author      : Zuguang Liu
# Date        : 2019-03-28 22:30:00
# Python Ver  : 3.6
# Description :

from email_read import *
from google_cal import *
import logging
import datetime
import os

#Keep a good log file
logname=os.getcwd()+'/logs/'+str(datetime.date.today())+'.log' #current directory+scanning date+extension
logging.basicConfig(filename=logname,format='[%(asctime)s]%(levelname)s:%(message)s',level=logging.DEBUG)

#read_appts requests and give list of dict of appoitments, make_events take that and push to google calandar
#don't forget to make a UNSEEN marker before actual implementation
logging.info('########Scanning Period Starts########')
make_events(read_appts())
logging.info('########Scanning Period Ends########')