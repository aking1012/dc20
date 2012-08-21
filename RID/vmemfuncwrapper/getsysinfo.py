import ctypes

class SYSTEM_INFO_struct_A(ctypes.Structure):
    _fields_ = [
                ("wProcessorArchitecture", ctypes.c_int16),
                ("wReserved", ctypes.c_int16)
                ]
class SYSTEM_INFO_union_A(ctypes.Union):
    _fields_ = [
                ("dwOemId", ctypes.c_int32),
                ("", SYSTEM_INFO_struct_A)
                ]
class SYSTEM_INFO(ctypes.Structure):
    _fields_ = [
                ("", SYSTEM_INFO_union_A),
                ("dwPageSize", ctypes.c_int32),
                ("lpMinimumApplicationAddress", ctypes.c_int32),
                ("lpMaximumApplicationAddress", ctypes.c_int32),
                ("dwActiveProcessorMask", ctypes.c_int32),
                ("dwNumberOfProcessors", ctypes.c_int32),
                ("dwProcessorType", ctypes.c_int32),
                ("dwAllocationGranularity", ctypes.c_int32),
                ("wProcessorLevel", ctypes.c_int16),
                ("wProcessorRevision", ctypes.c_int32)
                ]

meminfo = {}
sysInfo = SYSTEM_INFO()
GetSystemInfo = ctypes.windll.kernel32.GetSystemInfo
GetSystemInfo(ctypes.byref(sysInfo))
step = sysInfo.dwPageSize
start = sysInfo.lpMinimumApplicationAddress
stop = sysInfo.lpMaximumApplicationAddress
meminfo['start'] = str(start)
meminfo['stop'] = str(stop)
meminfo['step'] = str(step)

