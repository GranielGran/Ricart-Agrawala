import sys
import time
import threading
import socket
import json
import cPickle as pickle

##################################################################################################################################
# Variabel declarations                                                                                                         #
##################################################################################################################################
REPLY = 0
REQUEST = 1
WANTED = 0
HELD = 1
RELEASED = 2

#Stores the information of the local process
localInfo =     { 
                    'procName':         None,
                    'procPID':          None,   
                    'procState':        None,   
                    'procTimestamp':    None,   
                    'procAddr':         None,   
                    'procRemotes':      None 
                }

defferedQueue = []  #Waiting to reply too
replyQueue    = []  #Awaiting replies from
msgThread = None

remoteAddresses = { } #Store the addresses of the other processes

MAXRECV = 4096 
DEBUG = False

##################################################################################################################################
#Auxillary functions                                                                                                            #
##################################################################################################################################
def MutexInit(localAddr, procPID, procName, remoteAddr, remoteName, numRemotes):
    if DEBUG: print 'Entering --> MutexInit\n'
    #Initalize the local process info
    localInfo['procName']        = procName
    localInfo['procPID']         = procPID
    localInfo['procState']       = RELEASED
    localInfo['procAddr']        = localAddr
    localInfo['procRemotes']     = numRemotes

    #splitting the remoteAddr and remoteName tuples into separate variables
    remoteAddr1, remoteAddr2 = remoteAddr
    remoteName1, remoteName2 = remoteName #Don't know if we need this

    #Add the other two processes addresses to a dictionary for access later
    remoteAddresses[remoteName1] = remoteAddr1
    remoteAddresses[remoteName2] = remoteAddr2

    #Create thread that is supposed to fork the messageListener function to run in the background 
    msgThread = threading.Thread(target = MessageListener)
    msgThread.start()
    if DEBUG: print 'Exiting --> MutexInit'


##################################################################################################################################
# Messaging Functions                                                                                                          #
##################################################################################################################################
def SendMessage(addr, message):
    if DEBUG: print 'Entering --> SendMessage\n'
    if DEBUG: print ('Sending message --> {0}').format(message['procInfo']['procName'])
    sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sendingSocket.sendto(str(message), addr)
    sendingSocket.close()

    if DEBUG: print 'Exiting --> SendMessage'
    return True

def MessageListener():
    listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listeningSocket.bind(localInfo['procAddr']) #Bind the socket to the local address

    while True:
        MessageHandler(listeningSocket.recv(MAXRECV))

def MessageHandler(message):
    remoteMessage = eval(message) #Convert the string we get back to a dictionary
    if remoteMessage['type'] == REQUEST: 
        if (remoteMessage['procInfo']['procTimestamp'] < localInfo['procTimestamp'] and localInfo['procState'] == WANTED) or localInfo['procState'] == HELD:
            if DEBUG: print ('Deffered message from --> {0}').format(remoteMessage['procInfo']['procName'])
            defferedQueue.append(remoteMessage['procInfo']['procAddr'])
        else:
            message = { 'type': REPLY, 'procInfo': localInfo}
            if DEBUG: print('Sent reply to --> {0}').format(remoteMessage['procInfo']['procName'])
            SendMessage(remoteMessage['procInfo']['procAddr'], message)
    
    if remoteMessage['type'] == REPLY:
        if DEBUG: print ('Reply recieved from --> {0}').format(remoteMessage['procInfo']['procName']) 
        replyQueue.remove(remoteMessage['procInfo']['procAddr'])

##################################################################################################################################
# Mutex Functions                                                                                                               #
##################################################################################################################################
def MutexLock(the_mutex):
    if DEBUG: print 'Entering --> MutexLock\n'
    localInfo['procState'] = WANTED             #Change state
    localInfo['procTimestamp'] = time.time()    #Generate the timestamp for the message
    requestMessage = { 'type': REQUEST, 'procInfo': localInfo, 'mutex': the_mutex }

    #If we can't send any messages we assume that we are first and therefore can enter the section without any replies
    for address in remoteAddresses.values():
        SendMessage(address, requestMessage)
        replyQueue.append(address) #Only add addresses to the replyQueue if we sent a request to someone.
 
    while len(replyQueue) > 0: pass #Wait for the replyQueue to empty before continuing
    if DEBUG: print 'Exiting  -->  MutexLock'
    return True
    
    
def MutexUnlock(the_mutex):
    if DEBUG: print 'Entering --> MutexUnlock\n'
    localInfo['procState'] = RELEASED
    replyMessage = { 'type': REPLY, 'procInfo': localInfo, 'mutex': the_mutex }
    for address in replyQueue:
        SendMessage(address, replyMessage)
        defferedQueue.remove(address)
    
    if DEBUG: print 'Exiting  --> MutexUnlock'
    return True


def MutexExit():
    return True
