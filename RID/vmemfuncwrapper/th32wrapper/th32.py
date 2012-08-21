from ctypes import *
from th32reqtypes import *

#########################################################
# Modular toolhelp32 wrapper by aking1012.com@gmail.com #
#      Just my opinion of how it should be done         #
#########################################################

#Function arg structures
class structCreateToolHelp32Snapshot(Structure):
    _fields_ = [
                ("dwFlags", DWORD),
                ("th32ProcessID", DWORD)
                ]
    
class structHeap32First(Structure):
    _fields_ = [
                ("lphe", LPHEAPENTRY32),
                ("th32ProcessID", DWORD),
                ("th32HeapID", th32HeapID)
                ]
    
class structHeap32Next(Structure):
    _fields_ = [
                ("lphe", LPHEAPENTRY32)
                ]
    
class structHeap32ListFirst(Structure):
    _fields_ = [
                ("hSpanshot", HANDLE),
                ("lphl", LPHEAPLIST32)
                ]
    
class structHeap32ListNext(Structure):
    _fields_ = [
                ("hSpanshot", HANDLE),
                ("lphl", LPHEAPLIST32)
                ]
    
class structModule32First(Structure):
    _fields_ = [
                ("hSnapshot", HANDLE),
                ("lpme", LPMODULEENTRY32)
                ]
    
class structModule32Next(Structure):
    _fields_ = [
                ("hSnapshot", HANDLE),
                ("lpme", LPMODULEENTRY32)
                ]
    
class structProcess32First(Structure):
    _fields_ = [
                ("hSnapshot", HANDLE),
                ("lppe", LPPROCESSENTRY)
                ]
    
class structProcess32Next(Structure):
    _fields_ = [
                ("hSnapshot", HANDLE),
                ("lppe", LPPROCESSENTRY)
                ]
    
class structThread32First(Structure):
    _fields_ = [
                ("hSnapshot", HANDLE),
                ("lpte", LPTHREADENTRY32)
                ]
    
class structThread32Next(Structure):
    _fields_ = [
                ("hSnapshot", HANDLE),
                ("lpte", LPTHREADENTRY32)
                ]
    
class structToolhelp32ReadProcessMemory(Structure):
    _fields_ = [
                ("th32ProcessID", DWORD),
                ("lpBaseAddress", DWORD),
                ("lpBuffer", LPVOID),
                ("cbRead", SIZE_T),
                ("lpNumberIfBytesRead", SIZE_T)
                ]

#Getting the empty structs
#Getting our proc struct
def getProcStruct():
    aproc = structPROCESSENTRY(int(sizeof(structPROCESSENTRY)), 0, 0, 0, 0, 0, 0, 0, 0, '')
    return aproc

#Getting our heap structs
def getHeapStructs():
    return getHeapListStruct(), getHeapStruct()
def getHeapStruct():
    return structHEAPENTRY(sizeof(structHEAPENTRY), 0, 0, 0, 0, 0, 0, 0, 0)
def getHeapListStruct():
    return structHEAPLIST(sizeof(structHEAPLIST), 0, 0, HF32_DEFAULT)

#Getting our module structs
def getModuleStruct():
    return structMODULEENTRY(sizeof(structMODULEENTRY), 0, 0, 0, 0, 0, 0, 0, '', '') 
    

#APIs
#Get the snapshot
def CreateToolHelp32Snapshot(dwFlags, PID):
    arg = structCreateToolHelp32Snapshot(dwFlags, PID)
    handle = WinDLL("kernel32").CreateToolhelp32Snapshot(arg)
    return handle

#Enumerate processes
def Process32First(structProcess32First):
    return WinDLL("kernel32").Process32First(structProcess32First)
def Process32Next(structProcess32Next):
    return WinDLL("kernel32").Process32Next(structProcess32Next)

#Walk the heaps
def Heap32ListFirst(structHeap32ListFirst):
    return WinDLL("kernel32").Heap32ListFirst(structHeap32ListFirst)
def Heap32ListNext(structHeap32ListNext):
    return WinDLL("kernel32").Heap32ListNext(structHeap32ListNext)
def Heap32First(structHeap32First):
    return WinDLL("kernel32").Heap32First(structHeap32First)
def Heap32Next(structHeap32Next):
    return WinDLL("kernel32").Heap32Next(structHeap32Next)

#Walking the modules
def Module32First(structModule32First):
    return WinDLL("kernel32").Module32First(structModule32First)
def Module32Next(structModule32Next):
    return WinDLL("kernel32").Module32Next(structModule32Next)

#Read process memory
def Toolhelp32ReadProcessMemory(structToolhelp32ReadProcessMemory):
    return WinDLL("kernel32").Toolhelp32ReadProcessMemory(structToolhelp32ReadProcessMemory)

#Threads
def Thread32First(structThread32First):
    return WinDLL("kernel32").Thread32First(structThread32First)
def Thread32Next(structThread32Next):
    return WinDLL("kernel32").Thread32Next(structThread32Next)

