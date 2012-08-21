from vmemreqtypes import *

#Function Structs
class structPrefetchVirtualMemory(Structure):
    #Much of this isn't tested...I just like to have it here in case I to flesh it in
    _fields_ = [
                ("dwSize", SIZE_T),
                ("hProcess", HANDLE) ,
                ("NumberOfEntries", ULONG_PTR),
                ("VirtualAddresses", PWIN32_MEMORY_RANGE_ENTRY),
                ("Flags", ULONG_PTR), 
                ]
class structVirtualAlloc(Structure):
    _fields_ = [
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ("flAllocationType", DWORD),
                ("flProtect", DWORD)
                ]
class structVirtualAllocEx(Structure):
    _fields_ = [
                ("hProcess", HANDLE),
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ("flAllocationType", DWORD),
                ("flProtect", DWORD)
                ]
class structVirtualAllocExNuma(Structure):
    _fields_ = [
                ("hProcess", HANDLE),
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ("flAllocationType", DWORD),
                ("flProtect", DWORD),
                ("nndPreferred", DWORD)
                ]
class structVirtualFree(Structure):
    _fields_ = [
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ("dwFreeType", DWORD)
                ]
class structVirtualFreeEx(Structure):
    _fields_ = [
                ("hProcess", HANDLE),
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ("dwFreeType", DWORD)
                ]

class structVirtualLock(Structure):
    _fields_ = [
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ]
class structVirtualUnlock(Structure):
    _fields_ = [
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ]
class structVirtualProtect(Structure):
    _fields_ = [
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ("flNewProtect", DWORD),
                ("flOldProtect", DWORD),
                ]
class structVirtualProtectEx(Structure):
    _fields_ = [
                ("hProcess", HANDLE),
                ("lpAddress", LPVOID),
                ("dwSize", SIZE_T),
                ("flNewProtect", DWORD),
                ("flOldProtect", DWORD),
                ]
class structVirtualQuery(Structure):
    _fields_ = [
                ("lpAddress", LPVOID),
                ("lpAddress", PMEMORY_BASIC_INFORMATION),
                ("dwLength", SIZE_T)
                ]
class structVirtualQueryEx(Structure):
    _fields_ = [
                ("hProcess", HANDLE),
                ("lpAddress", LPVOID),
                ("lpAddress", PMEMORY_BASIC_INFORMATION),
                ("dwLength", SIZE_T)
                ]


#Function Calls
def PrefetchVirtualMemory():
    return
def VirtualAlloc():
    return
def VirtualAllocEx():
    return
def VirtualAllocExNuma():
    return
def VirtualFree():
    return
def VirtualFreeEx():
    return
def VirtualLock():
    return
def VirtualUnlock():
    return
def VirtualProtect():
    return
def VirtualProtectEx():
    return
def VirtualQuery():
    return
def VirtualQueryEx():
    return