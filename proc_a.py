import sys
import RicartAgrawala
import time

RicartAgrawala.MutexInit(('127.0.0.1', 5551), 1, 'proc_a', ((('127.0.0.1', 5552), ('127.0.0.1', 5553))), ('proc_b', 'proc_c'), 2)
RicartAgrawala.MutexLock('Mutex')
print 'proc_a\n'
time.sleep(2)
RicartAgrawala.MutexUnlock('Mutex')
time.sleep(10)
RicartAgrawala.MutexExit()
