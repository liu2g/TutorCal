# Author      : Zuguang Liu
# Date        : 2019-03-30 05:44:22
# Python Ver  : 3.6
# Description : 

from read_email import *
from google_cal import *
import logging

#Keep a good log file
logging.basicConfig(filename='controlV2.log',format='[%(asctime)s]%(levelname)s:%(message)s',level=logging.DEBUG)


make_events(read_appts())