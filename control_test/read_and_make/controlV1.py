# Author      : Zuguang Liu
# Date        : 2019-03-28 23:27:10
# Python Ver  : 3.6
# Description : First controller that connects reading email and making goole events

from read_email import *
from google_cal import *

# read_appts returns a list of dict, each dict details the appointment
# make_event takes that dict and makes the event

for appt in read_appts():
	make_event(appt)