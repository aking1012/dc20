import ctypes
from getsysinfo import *
verbose = 0
def log(astring):
    print astring
###############################################
#    I got really bored prototyping functions,#
#        so I just call them when I can in    #
#        in this part.                        #
#    And yes, cut the bitching, I re-used some#
#        code...                              #
###############################################
VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
VirtualQueryEx = ctypes.windll.kernel32.VirtualQueryEx
VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
OpenProcess = ctypes.windll.kernel32.OpenProcess
ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
CloseHandle = ctypes.windll.kernel32.CloseHandle

memAddDict = {}
MEM_RESERVE = 0x2000
MEM_COMMIT = 0x1000
PAGE_READWRITE = 0x4
PROCESS_ALL_ACCESS = 0x1f0fff

DWORD = ctypes.c_uint
SIZE_T = DWORD
HANDLE = ctypes.c_void_p
ULONG_PTR = DWORD
HMODULE = DWORD
th32HeapID = DWORD
LPCVOID = ctypes.POINTER(DWORD)
LPVOID = ctypes.c_void_p
PVOID = ctypes.c_void_p


class structMEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
                ('BaseAddress',  ctypes.c_uint),  
                ('AllocationBase',  ctypes.c_uint),  
                ('AllocationProtect',  DWORD),  
                ('RegionSize',  SIZE_T), 
                ('State',  DWORD),  
                ('Protect',  DWORD),  
                ('Type',  DWORD)  
                ]

PMEMORY_BASIC_INFORMATION = ctypes.POINTER(structMEMORY_BASIC_INFORMATION)

class structVirtualQueryEx(ctypes.Structure):
    _fields_ = [
                ('hProcess', HANDLE),
                ('lpAddress', ctypes.c_uint),
                ('lpBuffer', PMEMORY_BASIC_INFORMATION),
                ('dwLength', SIZE_T)
                ]
class ReadProcessMemory(ctypes.Structure):
    _fields_ = [
                ('hProcess', HANDLE),
                ('lpBaseAddress', ctypes.c_uint),
                ('lpBuffer', ctypes.c_char_p),
                ('nSize', ctypes.c_uint),
                ('lpNumberOfBytesRead', ctypes.c_uint)
                ]

import ctypes
import ctypes.wintypes
kernel32 = ctypes.wintypes.windll.kernel32

class Access:
    DELETE      = 0x00010000
    READ_CONTROL= 0x00020000
    SYNCHRONIZE = 0x00100000
    WRITE_DAC   = 0x00040000
    WRITE_OWNER = 0x00080000
    PROCESS_VM_WRITE = 0x0020
    PROCESS_VM_READ = 0x0010
    PROCESS_VM_OPERATION = 0x0008
    PROCESS_TERMINATE = 0x0001
    PROCESS_SUSPEND_RESUME = 0x0800
    PROCESS_SET_QUOTA = 0x0100
    PROCESS_SET_INFORMATION = 0x0200
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_DUP_HANDLE = 0x0040
    PROCESS_CREATE_THREAD = 0x0002
    PROCESS_CREATE_PROCESS = 0x0080

def toggle_rwx(pid, address):
    '''
    '''
    

def read_process_mem(pid, address, size):
    """Read memory of the specified process ID."""
    buf = ctypes.create_string_buffer(size)
    gotBytes = ctypes.c_ulong(0)
    h = kernel32.OpenProcess(Access.PROCESS_VM_READ, False, pid)
    try:
        #if kernel32.ReadProcessMemory(h, address, buf, size, ctypes.byref(gotBytes)):
        kernel32.ReadProcessMemory(h, address, buf, size, ctypes.byref(gotBytes))
        kernel32.CloseHandle(h)
        return buf
        #else:
        #    # TODO: report appropriate error GetLastError
        #    kernel32.CloseHandle(h)
        #    raise Exception("Failed to access process memory.")
    except:
        pass


def getVirtualQueryStructs():
    stMEMORY_BASIC_INFORMATION = structMEMORY_BASIC_INFORMATION(0, 0, 0, 0, 0, 0, 0)
    stVirtualQueryEx = structVirtualQueryEx(0, 0, ctypes.pointer(stMEMORY_BASIC_INFORMATION), ctypes.sizeof(stMEMORY_BASIC_INFORMATION))
    return stMEMORY_BASIC_INFORMATION, stVirtualQueryEx

def checkProcessVirtualAllocs(procHandle, key, bigdict):
    bigdict[key]['Findings']['VirtualQueryDetails']={}
    addresses = []
    step = int(meminfo['step'])
    start = int(meminfo['start'])
    stop = int(meminfo['stop'])
    stMEMORY_BASIC_INFORMATION, stVirtualQueryEx = getVirtualQueryStructs()
    stVirtualQueryEx.hProcess = procHandle
    stVirtualQueryEx.lpAddress = start
    while(start<stop):
        VirtualQueryEx(stVirtualQueryEx)
        if stMEMORY_BASIC_INFORMATION.BaseAddress:
            addresses.append([int(stMEMORY_BASIC_INFORMATION.BaseAddress), int(stMEMORY_BASIC_INFORMATION.RegionSize)])
            start = int(stMEMORY_BASIC_INFORMATION.BaseAddress) + int(stMEMORY_BASIC_INFORMATION.RegionSize) - step
            overusingdicts = {}
            overusingdicts['AllocationBase'] = stMEMORY_BASIC_INFORMATION.AllocationBase
            overusingdicts['AllocationProtect'] = stMEMORY_BASIC_INFORMATION.AllocationProtect
            overusingdicts['RegionSize'] = stMEMORY_BASIC_INFORMATION.RegionSize
            overusingdicts['State'] = stMEMORY_BASIC_INFORMATION.State
            overusingdicts['Protect'] = stMEMORY_BASIC_INFORMATION.Protect
            overusingdicts['Type'] =  stMEMORY_BASIC_INFORMATION.Type
            bigdict[key]['Findings']['VirtualQueryDetails'][stMEMORY_BASIC_INFORMATION.BaseAddress] = overusingdicts
        start += step
        stVirtualQueryEx.lpAddress = start            
    return addresses, bigdict

def cleanProcessVirtualAllocs(bigdict, key, addresses):
    retvals = []
    eliminate = []
    addrs=[]
    noret=[]
    try:
        for module in bigdict[key]['Modules']:
            temp = []
            temp.append(int(module['PTRmodBaseAddr']))
            end = int(module['PTRmodBaseAddr'])+int(module['modBaseSize'])
            temp.append(end)
            eliminate.append(temp)
    except:
        pass
    for pair in addresses:
        addrs.append(pair[0])
    for alloc in addrs:
        for elim in eliminate:
            if elim[0] <= alloc <= elim[1]:
                noret.append(alloc)
            #parse the range better...identify thread data without a debugger?
            elif alloc < int(0x400000):
                noret.append(alloc)
            #parse the range better...identify thread data without a debugger?
            elif alloc > int(0x7FFC0000):
                noret.append(alloc)
            #ignore memory mapped files
            elif bigdict[key]['Findings']['VirtualQueryDetails'][alloc]['Type']==0x40000:
                noret.append(alloc)
            #ignore null types
            elif bigdict[key]['Findings']['VirtualQueryDetails'][alloc]['Type']==0x0:
                noret.append(alloc)
            else:
                pass
    for alloc in addrs:
        if alloc not in noret:
            retvals.append(alloc)
    return retvals

def debugMSFWitchery(bigdict):
    '''
    '''
    

def lookForHeaders(bigdict):
    count = 0
    for key in bigdict.keys():
        if key:
            try:
                mem = bigdict[key]['Findings']['VirtualQueryResults']
                for address in mem:
                    try:
                        amem = read_process_mem(int(key), address, 8)
                        if amem.value[:2] == 'MZ':
                            try:
                                log('maybe header found in: ' + key + ' at address: ' + hex(address))
                                for key in bigdict[key]['Findings']['VirtualQueryDetails'].keys():
                                    if abs(int(key) - address) < 10000:
                                        count += 1
                            except:
                                pass
                            try:
                                bigdict[key]['FoundHeader'] = bigdict[key]['FoundHeader'].append(address) 
                            except:
                                bigdict[key]['FoundHeader'] = []
                                bigdict[key]['FoundHeader'] = bigdict[key]['FoundHeader'].append(address)                                 
                    except:
                        pass
            except:
                pass
    return

def slowCheck(bigdict):
    couldNot = ''
    for key in bigdict.keys():
        if key:
            procHandle = OpenProcess(PROCESS_ALL_ACCESS, 1, int(key))
            str_addr = VirtualAllocEx ( procHandle , 0, 1, MEM_RESERVE|MEM_COMMIT, PAGE_READWRITE )
            if str_addr:
                addresses, bigdict = checkProcessVirtualAllocs(procHandle, key, bigdict)
                bigdict[key]['Findings']['VirtualQueryResults'] = addresses

                adds = cleanProcessVirtualAllocs(bigdict, key, addresses)
                bigdict[key]['Findings']['VirtualQueryResults'] = adds
            else:
                couldNot = couldNot + bigdict[key]['Name'] + ', '
            VirtualFreeEx ( procHandle ,str_addr , 0, 0x8000 )
    lookForHeaders(bigdict)
    if verbose:
        print "\nCould not allocate memory in " + couldNot[0:-2] + '.'
        print '\nA commercial tool would need to do privilege escalation to do this.  Simply copy bits from meterpreter getsystem to use its tricks'
    return bigdict