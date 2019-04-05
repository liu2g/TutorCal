# Author      : Zuguang Liu
# Date        : 2019-03-30
# Python Ver  : 3.6
# Description :

import inspect

def foo():
	print(inspect.stack()[0][3])

foo()