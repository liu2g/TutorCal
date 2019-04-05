# Author      : Zuguang Liu
# Date        : 2019-03-30 04:28:33
# Python Ver  : 3.6
# Description : 

import logging
logging.basicConfig(filename='example.log',format='[%(asctime)s]%(levelname)s:%(message)s',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
