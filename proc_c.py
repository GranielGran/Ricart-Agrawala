import sys
import RicartAgrawala
import time

RicartAgrawala.MutexInit(('127.0.0.1', 5553), 3, 'proc_c', ((('127.0.0.1', 5551), ('127.0.0.1', 5552))), ('proc_a', 'proc_b'), 2)
time.sleep(6)
RicartAgrawala.MutexLock('Mutex')
print 'proc_c\n'
time.sleep(2)
RicartAgrawala.MutexUnlock('Mutex')
time.sleep(10)
