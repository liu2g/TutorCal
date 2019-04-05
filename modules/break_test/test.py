# Author      : Zuguang Liu
# Date        : 2019-03-30 05:01:31
# Python Ver  : 3.6
# Description : 

import logging

def make_it_pass(n):
	print('passed value', n)
	if n<15:
		raise Exception('You shall not pass')
	return []

i=0
while True:
	try:
		make_it_pass(i)
	except Exception as e:
		if i<10:
			i+=1
			continue
		else:
			logging.warning('No, %s',e)
	break