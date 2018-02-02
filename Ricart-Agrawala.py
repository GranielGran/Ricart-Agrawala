from collections import namedtuple
from enum import Enum
from datetime import datetime
import threading
from socket import socket

##################################################################################################################################
# Variabel deklarationer                                                                                                         #
##################################################################################################################################
class procStates(Enum):
    WANTED = 0
    HELD = 1
    RELEASED = 2

class msgTypes(Enum):
    REPLY = 0
    REQUEST = 1

#class msgTypes(Enum):
#    REQUEST = 0
#    REPLY = 1

#localInfo lagrar information om the locala processen
localInfo =     { 
                    'procName':         None,
                    'procPID':          None,   
                    'procState':        None,   
                    'procTimestamp':    None,   
                    'procAddr':         None,   
                    'procRemotes':      None, 
                }

#mutexQueue =   {   
#                    'proc_a': statetable['proc_a'], 
#                    'proc_b': statetable['proc_b'],
#                    'proc_c': statetable['proc_c']
#                }

defferedQueue = []  #Waiting to reply too
replyQueue    = []  #Awaiting replies from
messageListener      =   None

remoteAddresseses = { }

MAXRECV = 4096 #Amounts of bytes to receieve from a 

##################################################################################################################################
#Auxillary funktioner                                                                                                            #
##################################################################################################################################
def MutexInit(localAddr, procPid, procName, remoteAddr, remoteName, numRemotes):
    #Initalize the local process info
    localInfo['procName']        = procName
    localInfo['procPID']         = procPID
    localInfo['procState']       = procStates.RELEASED
    localInfo['procAddr']        = localAddr
    localInfo['procRemotes']     = numRemotes

    #splitting the remoteAddr and remoteName tuples into separate variables
    remoteAddr1, remoteAddr2 = remoteAddr
    remoteName1, remoteName2 = remoteName #Don't know if we need this

    #Add the other two processes addresses to a dictionary for access later
    remoteAddresses[remoteName1] = remoteAddr1
    remoteAddresses[remoteName2] = remoteAddr2

    #Create thread that is supposed to fork the messageListener function to run in the background 
    msgThread = threading.Thread(target = messageListener, args = remoteAddresses)


##################################################################################################################################
# Meddelande funktioner                                                                                                          #
##################################################################################################################################
def SendMessage(addr, message):
    sendingSocket = socket.socket(family=AF_INET, type=SOCK_STREAM) 
    if not sendingSocket.connect(addr): return False  
    sendingSocket.send(message)
    sendingSocket.close()

    return True

def MessageListener():
    listeningSocket = socket(AF_INET, SOCK_STREAM)
    listeningSocket.bind(procInfo[procAddr]) #Bind the socket to the local address
    listeningSocket.listen(localInfo['procRemotes'])

    while 1:
        (clientSocket, addr) = listeningSocket.accept()
        messageHandler(listeningSocket.recv(MAXRECV))

def MessageHandler(remoteMessage):
    if remoteMessage['type'] == msgTypes.REQUEST:
        if remoteMessage['procInfo']['procTimestamp'] < localInfo['procTimestamp'] or localInfo['procState'] == procStates.HELD:
            defferedQueue[remoteMessage['procInfo']['procName']] = remoteMessage['procInfo']['procName']
        else:
            message = { 'type': msgTypes.REPLY, 'procInfo': localInfo, 'mutex': mutex }
            SendMessage(remoteMessage['procInfo']['procAddr'], message)
    
    if remoteMessage['type'] == msgTypes.REPLY:
        replyQueue.remove(remoteMessage['procInfo']['procName'])

##################################################################################################################################
# Mutex Funktioner                                                                                                               #
##################################################################################################################################
     

def GetMutexLock(mutex):
    procInfo['procState'] = procStates.WANTED
    localInfo['procTimestamp'] = datetime.now #generate the timestamp for the message
    requestMessage = { 'type': msgTypes.REQUEST, 'procInfo': localInfo, 'mutex': mutex }

    #If we can't send any messages we assume that we are first and therefore can enter the section without any replies
    for address in remoteAddresses:
        if SendMessage(address, message): 
            replyQueue.update(address) #Only add addresses to the replyQueue if we sent a request to someone.
 
    while replyQueue > 0: pass #Wait for the replyQueue to empty before continuing
    return True
    
    
def ReleaseMutexLock(mutex):
    procInfo['procState'] = procStates.RELEASED
    replyMessage = { 'type': msgTypes.REPLY, 'procInfo': localInfo, 'mutex': mutex }
    for address in replyQueue:
        SendMessage(address, replyMessage)
    
    return True

def MutexExit():
    return True