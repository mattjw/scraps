# 
#

import time
import datetime
import sys

print "starting..."
for _ in xrange(10):
    now = datetime.datetime.today()
    print "std %s" % now
    sys.stderr.write('err %s\n' % now)
    time.sleep(1)
print "...successfully finishing"