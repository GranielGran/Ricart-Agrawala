import sys
import RicartAgrawala
import time

RicartAgrawala.MutexInit(('127.0.0.1', 5552), 2, 'proc_b', (('127.0.0.1', 5551), ('127.0.0.1', 5553)), ('proc_a', 'proc_c') , 2)
time.sleep(5)
RicartAgrawala.MutexLock('Mutex')
print 'proc_b\n'
time.sleep(2)
RicartAgrawala.MutexUnlock('Mutex')
time.sleep(10)
