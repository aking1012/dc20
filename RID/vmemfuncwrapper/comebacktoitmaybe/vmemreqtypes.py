from ctypes import *

#Types
DWORD = c_uint
SIZE_T = DWORD
HANDLE = DWORD
ULONG_PTR = c_ubyte
LPVOID = c_void_p
PVOID = c_void_p
LONG = c_long
TCHAR = c_char
MAX_PATH = 260
BOOL = c_bool
PHANDLE = POINTER(HANDLE)
TOKEN_ADJUST_PRIVILEGES = 32
TOKEN_QUERY = 8
CUSTOM_TOKEN_START = TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY

#Structs
class structWIN32_MEMORY_RANGE_ENTRY(Structure):
    _fields_ = [
                ("VirtualAddress", PVOID),
                ("NumberOfBytes", SIZE_T)
                ]

class structMEMORY_BASIC_INFORMATION(Structure):
    _fields_ = [
                ("BaseAddressAddress", PVOID),
                ("AllocationBase", PVOID),
                ("AllocationProtect", DWORD),
                ("RegionSize", SIZE_T),
                ("State", DWORD),
                ("Protect", DWORD),
                ("Type", DWORD),
                ]
class structPROCESSENTRY(Structure):
    _fields_ = [
                ("dwSize", DWORD),
                ("cntUsage", DWORD),
                ("th32ProcessID", DWORD),
                ("th32DefaultHeapID", ULONG_PTR),
                ("th32ModuleID", DWORD),
                ("cntThreads", DWORD),
                ("th32ParentProcessID", DWORD),
                ("pcPriClassBase", LONG),
                ("dwFlags", DWORD),
                ("szExeFile", TCHAR * MAX_PATH)
                ]

class LUID(Structure):
    _fields_ = [
                ("LowPart",     DWORD),
                ("HighPart",    LONG)
                ]
class LUID_AND_ATTRIBUTES(Structure):
    _fields_ = [
                ("Luid",        LUID),
                ("Attributes",  DWORD)
                ]
class TOKEN_PRIVILEGES(Structure):
    _fields_ = [
                ("PrivilegeCount",  DWORD),
                ("Privileges",      LUID_AND_ATTRIBUTES)
                ]

#Derived types
PWIN32_MEMORY_RANGE_ENTRY = POINTER(structWIN32_MEMORY_RANGE_ENTRY)
PMEMORY_BASIC_INFORMATION = POINTER(structMEMORY_BASIC_INFORMATION)
PLUID = POINTER(LUID)
PTOKEN_PRIVILEGES = POINTER(TOKEN_PRIVILEGES)

#Req Functions
#Structs
class structOpenProcessToken(Structure):
    _fields_ = [            
                ("ProcessHandle", HANDLE),
                ("DesiredAccess", DWORD),
                ("TokenHandle", PHANDLE)
                ]
class structOpenProcess(Structure):
    _fields_ = [
                ("TOKEN", DWORD),
                ("TRUEFALSE", BOOL),
                ("PID", DWORD)
                ]
class structCloseHandle(Structure):
    _fields_ = [
                ("hProcess", HANDLE)
                ]

#Functions
def GetCurrentProcess():
    return WinDLL("kernel32").GetCurrentProcess()
def OpenProcessToken(structOpenProcessToken):
    return
