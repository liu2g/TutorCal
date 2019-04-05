# Author      : Zuguang Liu
# Date        : 2019-03-28 22:30:00
# Python Ver  : 3.6
# Description : 

import pandas

def find_class(code):
	df=pandas.read_csv('lookup_table.csv',header=None)
	codel=df[0].tolist()
	namel=df[1].tolist()
	try:
		i=codel.index(code)
		return namel[i]
	except ValueError:
		return code

print(find_class('MATH1062'))