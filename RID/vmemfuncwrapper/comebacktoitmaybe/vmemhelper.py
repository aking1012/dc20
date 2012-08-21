from vmem import *

token = ''

def virtualQueryExAllQuick(bigdict):
    token = getMaxToken()
    for PID in bigdict.keys():
        addresses = doSeveralVirtualAllocs(PID, token)
        doRegression(addresses)
        doScanSixRange(bigdict)
    return


def doSeveralVirtualAllocs(PID, token):
    return
def doRegression(addresses):
    return
def doScanSixRange(bigdict):
    return

def getVirtualAllocNoReqAndFree(PID, token):
    address = ''
    return address

def getPageSize(bigdict):
    return


def getMaxToken():
    this = structOpenProcessToken(GetCurrentProcess(), CUSTOM_TOKEN_START, 0)

    token = OpenProcessToken()
    return token