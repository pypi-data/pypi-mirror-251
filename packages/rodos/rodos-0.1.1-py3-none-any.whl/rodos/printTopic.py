# rodos-middleware: This file is a part of the Master Thesis of Sebastian Kind 2023

#!/bin/python3
import struct

# Sebastian Kind 2023 Python3 Rodos-Middleware


import os
import atexit
import subprocess
import sys
import signal
import traceback

from .topic import *

logging_enabled = True
fileList = []
subProcessThreadIdList = []
plist = []


def closeFiles():
    for k in thread2fifoDict:
        try:
            os.remove(thread2fifoDict[k]) # remove FIFOs/named pipes
        except FileNotFoundError:
            pass
    for p in plist: #terminate monitors e.g. xterm
        p.terminate()
        p.kill()

atexit.register(closeFiles)

def sigHandler(signo, frame):
    closeFiles()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigHandler)
#signal.signal(signal.SIGINT, sigHandler)



# @atexit.register
# def closeProcesses():
#     for p in plist:
#         p.terminate()

# def noLogging():
#     for p in plist: #terminate monitors e.g. xterm
#         p.terminate()
#         p.kill()
#     closeFiles()


thread2fifoDict = {}
def getOrCreateFIFO(threadID: int) -> str:
    """

    :param threadID: unique ID of a C++RODOS-Thread that is printing something. This is ID is used to create a unique
    FIFO(named pipe) that collects the thread's debug output
    :return: return the filename of the FIFO, relative path for now
    """
    if threadID not in thread2fifoDict:
        #thread not known, add it to the dict
        FIFOName = "./RodosThread"+str(threadID)
        try:
            os.remove(FIFOName)
        except FileNotFoundError:
            pass
        os.mkfifo(FIFOName, 0o666)
        thread2fifoDict[threadID] = FIFOName
    #thread known or added
    return thread2fifoDict[threadID]

# def print_topic_handler(data):
#     callback_thread = threading.Thread(target=_print_topic_handler, args=(data,))
#     callback_thread.run()

def openMonitor(threadID: int, fifoName: str):
    if threadID in subProcessThreadIdList:
        return
    subProcessThreadIdList.append(threadID)
    command_to_run = "xterm -e 'tail -f {}' &".format(fifoName)
    proc = subprocess.Popen(command_to_run, shell=True)

    plist.append(proc) # close it on exit




def _print_topic_handler(data):

    """

    :param data: called by caller of callback
    :return: nothing

    print_topic_handler get a variable length structure with leading 8 bytes of meta data, first uint32 denoting the
    sending thread, second uint32 containting the length of the whole print-message including the meta data. The actual
    print message starts at the 9th byte (index 8)

    each thread should get it's own named pipe/serial monitor/whatever to list show the output in a terminal
    """
    try:
        unpacked = struct.unpack("ii", bytes(data[:8]))

       # print("id =", unpacked[0], "length = ", unpacked[1])
        threadID = unpacked[0]
        length = unpacked[1]


        fifoName = getOrCreateFIFO(threadID)
        #print("printtopic data:", data[8:length+8])

        openMonitor(threadID, fifoName)

        try:
            with open(fifoName, "wb") as fifo:
                fifo.write(data[8:length + 8])
        except Exception as e:
            print(f"Error writing to FIFO: {e}")





    except Exception as error:
        print("printtopic exception", type(error).__name__)

        traceback.print_exc()
    pass

if logging_enabled:
    print_topic = Topic(11)
    print_topic.addSubscriber(_print_topic_handler)