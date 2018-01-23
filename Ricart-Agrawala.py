from collections import namedtuple
from enum import enum
import datetime
import threading
import socket
import json



##################################################################################################################################
# Daniels Mysteriska Notes                                                                                                       #
##################################################################################################################################
#Vissa saker kan vara redundanta, om du hittar något så skicka koden som är motsägande till mig på Discord
#Om jag inte ser det direkt eller tar lite tid att svara så föröska kolla på något annat

#Kom ihåg att python har bra documentation för saker så sök, sök, sök
#Ändra hur mycket du vill det här är bara ideer jag hade

#Tror att kruxet verkligen ligger i att lista ut hur meddelande ska gå runt sen så blir det ganska simpelt

##################################################################################################################################
# Variabel deklarationer                                                                                                         #
##################################################################################################################################
#En Enum för att märka olika typer av meddelande. du använder den så här verkar det som messageType.WANTED eller vilken du nu vill använda
class stateTypes(Enum):
    WANTED = 1
    HELD = 2
    REQUEST = 3
    REPLY = 4
    RELEASED = 5

#Kolla upp hur namedtuples, fungerar ungefär som en struct i c.
#Hade ideen för dessa när vi började så vet inte om de blir så bra
mutexState      =   namedtuple('State', 'state prio replylst')
mutexPriority   =   namedtuple('Priority', 'timestamp pid')
mutexMessage    =   namedtuple('Message', 'msgtype mutexname prio')

#Använda denna för att se 
stateTable =    {  
                    'proc_a': mutexState(state = None, prio = None, replylst = None), 
                    'proc_b': mutexState(state = None, prio = None, replylst = None),
                    'proc_c': mutexState(state = None, prio = None, replylst = None)
                }

#Det här är en Dictionary, använder denna för att för att se hur det ligger till med de olika processerna, börjar med att alla requestar
#Sen så uppdaterar vi den när de får ett lås, släpper ett lås, om de väntar på replies osv. Use case --> mutexQueue['proc_a'] 
mutexQueue =   {   
                    'proc_a': statetable['proc_a'], 
                    'proc_b': statetable['proc_b'],
                    'proc_c': statetable['proc_c']
                }

#Kan eventuellt använda denna för att när vi vill skicka meddelande
processAddress = {'proc_a': ('192.168.0.50', '8000'), 'proc_b': ('192.168.0.50', '8001'), 'proc_c': ('192.168.0.50', '8002')}

#tänkte använda den här för att jämnföra mot ovanstående eller något.
int n_nodes = 3


##################################################################################################################################
#Auxillary funktioner                                                                                                            #
##################################################################################################################################
#Kallar på denna först för att skicka request messages till alla andra processer och lite annat eventuellt.
def MutexInit(ip, procport, procpid, procName):


def UpdateMutexQueue():
    
##################################################################################################################################
# Meddelande funktioner                                                                                                          #
##################################################################################################################################
#Den här tror jag vi kommer behöva för att skicka meddelande till andra processer.
def SendMessage(addr, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.send(message)
    s.close()

#Vet inte om vi kommer behöva den här.
def MessageHandler():
    request_socket = threading.thread
    if requestmessage.msgtype == "request":
        return 1
    else return 0
    replymessage = mutex_message()
    if replymessage.msgtype == "reply":
        return 1
    else return 0

##################################################################################################################################
# Mutex Funktioner                                                                                                               #
##################################################################################################################################
#Borde inte behöva vara mer avancerad än så här.
def MutexHeld():
    for n in mutexQueue.items():
        processName, state = n
        if stateTable[processName].state == stateTypes.HELD:
            return True
        return False      

def GetMutexLock(mutex);
    state = mutex_state(requested, datetime.datetime.now, None)
    return True

    if condition:
        return False

#Uppdatera eget mutexstate och skicka meddelande till alla andra processer state i meddeleandet så att de också kan uppdatera
def ReleaseMutexLock(mutex, pname):
    mutexState(state = stateTypes.RELEASED, prio = None, replylst = None),
    mutex_queue[pname] = 0
    return True

    if condition:
        return false

#Vette Fan
def MutexExit():