from ctypes import *

#########################################################
# Modular toolhelp32 wrapper by aking1012.com@gmail.com #
#      Just my opinion of how it should be done         #
#########################################################

#Just the types we need for our local class declarations
#Some constants for x86...might be different on x64
MAX_MODULE_NAME32 = 255
MAX_PATH = 260
TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
TH32CS_SNAPALL = TH32CS_SNAPHEAPLIST | TH32CS_SNAPMODULE | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD
snapopts = {"TH32CS_SNAPALL":TH32CS_SNAPALL, "TH32CS_SNAPHEAPLIST":TH32CS_SNAPHEAPLIST, "TH32CS_SNAPMODULE":TH32CS_SNAPMODULE, "TH32CS_SNAPPROCESS":TH32CS_SNAPPROCESS, "TH32CS_SNAPTHREAD":TH32CS_SNAPTHREAD}
HF32_DEFAULT = 1
HF32_SHARED = 2

#I know it's kind of ugly that I just used DWORD as a proto here a lot
#Also I used c_uint instead of wintypes, so I could do an import check on the linux side without a fail.
DWORD = c_uint
SIZE_T = DWORD
HANDLE = c_void_p
ULONG_PTR = DWORD
HMODULE = DWORD

BYTE_DEF = DWORD
LONG = c_long
TCHAR = c_char

#Types we need for our non-local type declarations
th32HeapID = DWORD
LPCVOID = POINTER(DWORD)
LPVOID = c_void_p

#Local class declarations
class structHEAPENTRY(Structure):
    _fields_ = [
                ("dwSize", SIZE_T),
                ("hHandle", HANDLE),
                ("dwAddress", ULONG_PTR),
                ("dwBlockSize", SIZE_T),
                ("dwFlags", DWORD),
                ("dwLockCount", DWORD),
                ("dwResvd", DWORD),
                ("th32ProcessID", DWORD),
                ("th32HeapID", ULONG_PTR)
                ]

class structHEAPLIST(Structure):
    _fields_ = [
                ("dwSize", SIZE_T),
                ("th32ProcessID", DWORD),
                ("t32HeapID", ULONG_PTR),
                ("dwFlags", DWORD)
                ]

class structMODULEENTRY(Structure):
    _fields_ = [
                ("dwSize", DWORD),
                ("th32ModuleID", DWORD),
                ("th32ProcessID", DWORD),
                ("GlblcntUsage", DWORD),
                ("ProccntUsage", DWORD),
                ("PTRmodBaseAddr", BYTE_DEF),
                ("modBaseSize", DWORD),
                ("hModule", HMODULE),
                ("szModule", TCHAR * (MAX_MODULE_NAME32 + 1)),
                ("szExePath", TCHAR * MAX_PATH)
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

class structTHREADENTRY(Structure):
    _fields_ = [
                ("dwSize", DWORD),
                ("cntUsage", DWORD),
                ("th32ThreadID", DWORD),
                ("th32OwnerProcessID", DWORD),
                ("tpBasePri", LONG),
                ("tpDeltaPri", LONG)
                ]

#Types derived from locally defined classes
LPHEAPENTRY32 = POINTER(structHEAPENTRY)
LPHEAPLIST32 = POINTER(structHEAPLIST)
LPMODULEENTRY32 = POINTER(structMODULEENTRY)
LPPROCESSENTRY = POINTER(structPROCESSENTRY)
LPTHREADENTRY32 = POINTER(structTHREADENTRY)
