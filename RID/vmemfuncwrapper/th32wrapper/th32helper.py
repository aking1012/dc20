from th32 import *
import os

#########################################################
# Modular toolhelp32 wrapper by aking1012.com@gmail.com #
#      Just my opinion of how it should be done         #
#  Warning: It reads like python, but it's not really   #
#    pythonic in that I don't return or set things      #
#             the way you would expect                  #
#########################################################

#Okay, there's a juvenile joke to be had there
bigdict = {}

#Snapping
def getSnapAll():
    return CreateToolHelp32Snapshot(snapopts['TH32CS_SNAPALL'], 0)
def getBigSnap(PID):
    snap = CreateToolHelp32Snapshot(snapopts['TH32CS_SNAPALL'], PID)
    return snap
def getCustomSnap(dwFlags, PID):
    snap = CreateToolHelp32Snapshot(dwFlags, PID)
    return snap


#Processes
def getFirstProcGeneric(snapHandle):
    aproc = getProcStruct()
    pproc = pointer(aproc)
    process = structProcess32First(snapHandle, pproc)
    if (Process32First(process)):
        return aproc
    else:
        quit()
        
def getNextProc(snapHandle, proc):
    process = structProcess32Next(snapHandle, pointer(proc))
    return Process32Next(process)

def eachProc(snapHandle, aproc):
    littledict = {}
    evenlittlerdict = {}
    
    littledict["Name"] = str(aproc.szExeFile)
    littledict["AddressInfo"] = {}
    littledict["Modules"] = {}
    littledict["Threads"] = {}
    littledict["Heaps"] = {}
    littledict["Findings"] = {}
    bigdict[str(aproc.th32ProcessID)] = littledict

def getProcs(snapHandle):
    aproc = getFirstProcGeneric(snapHandle)
    eachProc(snapHandle, aproc)
    while(getNextProc(snapHandle, aproc)):
        eachProc(snapHandle, aproc)
    return


#Heaps
def getHeapListAddresses(snapHandle):
    heapListStruct, heapStruct = getHeapStructs()
    pheaplist = pointer(heapListStruct)
    FirstHeapList = structHeap32ListFirst(snapHandle, pheaplist)
    Heap32ListFirst(FirstHeapList)
    str(heapStruct.th32ProcessID) + '.' + str(heapStruct.th32HeapID) + '.' + str(heapStruct.dwAddress)

    parseHeaps(snapHandle, heapListStruct, heapStruct)
    while(Heap32ListNext(FirstHeapList)):
        parseHeaps(snapHandle, heapListStruct, heapStruct)

def getHeapListAddress(snapHandle, heapListStruct, heapStruct):
    if bigdict[str(heapStruct.th32ProcessID)]['PID'] == str(os.getpid()):
        return
    pheap = pointer(heapStruct)
    FirstHeap = structHeap32First(pheap, heapListStruct.th32ProcessID, heapListStruct.t32HeapID)
    Heap32First(FirstHeap)
    str(heapStruct.th32ProcessID) + '.' + str(heapStruct.th32HeapID) + '.' + str(heapStruct.dwAddress)
    NextHeap = structHeap32Next(pheap)
    while(Heap32Next(NextHeap)):
        str(heapStruct.th32ProcessID) + '.' + str(heapStruct.th32HeapID) + '.' + str(heapStruct.dwAddress)
        
def getHeaps(snapHandle):
    heapListStruct, heapStruct = getHeapStructs()
    pheaplist = pointer(heapListStruct)
    FirstHeapList = structHeap32ListFirst(snapHandle, pheaplist)
    Heap32ListFirst(FirstHeapList)
    parseHeaps(snapHandle, heapListStruct, heapStruct)
    while(Heap32ListNext(FirstHeapList)):
        parseHeaps(snapHandle, heapListStruct, heapStruct)

def parseHeaps(snapHandle, heapListStruct, heapStruct):
    if bigdict[str(heapStruct.th32ProcessID)]['PID'] == str(os.getpid()):
        return
    pheap = pointer(heapStruct)
    FirstHeap = structHeap32First(pheap, heapListStruct.th32ProcessID, heapListStruct.t32HeapID)
    Heap32First(FirstHeap)
    arg = [heapStruct.hHandle, heapStruct.dwBlockSize]
    inEachHeapEntry(memcpyFromHeap(arg), str(heapStruct.th32ProcessID) + '.' + str(heapStruct.th32HeapID) + '.' + str(heapStruct.dwAddress))
    NextHeap = structHeap32Next(pheap)
    while(Heap32Next(NextHeap)):
        arg = [heapStruct.hHandle, heapStruct.dwBlockSize]
        inEachHeapEntry(memcpyFromHeap(arg), str(heapStruct.th32ProcessID) + '.' + str(heapStruct.th32HeapID) + '.' + str(heapStruct.dwAddress))

def memcpyFromHeap(arg):
    try:
        heapcontents = string_at(arg[0], arg[1])
    except:
        return ''
    return heapcontents

def inEachHeapEntry(heapData, fname):
    try:
        if heapData != '':
            with open('e:\\RID\\dumps\\' + fname + '.raw', 'wb') as f:
                f.write(heapData)
            found = 1
        else:
            found = 0
    except:
        found = 0
    return found

#Threads
#Not necessary in the release

#Modules
def getModLists(snapHandle):
    modStruct = getModuleStruct()
    getModFirst = structModule32First()
    getModFirst.lpme = pointer(modStruct)
    for PID in bigdict.keys():
        snapHandle = getCustomSnap(snapopts['TH32CS_SNAPMODULE'], int(PID))
        getModFirst.hSnapshot = snapHandle
        Module32First(getModFirst)
        littldict = {}
        alist = []
        littldict["dwSize"] = str(modStruct.dwSize)
        littldict["th32ModuleID"] = str(modStruct.th32ModuleID)
        littldict["th32ProcessID"] = str(modStruct.th32ProcessID)
        littldict["GlblcntUsage"] = str(modStruct.GlblcntUsage)
        littldict["ProccntUsage"] = str(modStruct.ProccntUsage)
        littldict["PTRmodBaseAddr"] = str(modStruct.PTRmodBaseAddr)
        littldict["modBaseSize"] = str(modStruct.modBaseSize)
        littldict["hModule"] = str(modStruct.hModule)
        littldict["szModule"] = str(modStruct.szModule)
        littldict["szExePath"] = str(modStruct.szExePath)
        alist.append(littldict)
        while(Module32Next(getModFirst)):
            littldict = {}
            littldict["dwSize"] = str(modStruct.dwSize)
            littldict["th32ModuleID"] = str(modStruct.th32ModuleID)
            littldict["th32ProcessID"] = str(modStruct.th32ProcessID)
            littldict["GlblcntUsage"] = str(modStruct.GlblcntUsage)
            littldict["ProccntUsage"] = str(modStruct.ProccntUsage)
            littldict["PTRmodBaseAddr"] = str(modStruct.PTRmodBaseAddr)
            littldict["modBaseSize"] = str(modStruct.modBaseSize)
            littldict["hModule"] = str(modStruct.hModule)
            littldict["szModule"] = str(modStruct.szModule)
            littldict["szExePath"] = str(modStruct.szExePath)
            alist.append(littldict)
        bigdict[PID]['Modules'] = alist
        #closeHandle
    return

def getModListAddresses(PID):
    modranges = []
    for mod in bigdict[PID]['Modules'].keys():
        amod = bigdict[PID]['Modules'][mod]
        modrange = [amod['th32ModuleID'], amod['PTRmodBaseAddr'], amod['PTRmodBaseAddr']]
        modranges.append(modrange)
    return modranges