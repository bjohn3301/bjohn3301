import ctypes
import win32api
import win32process
import win32con
import psutil

def find_process_id(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return proc.info['pid']
    return None

def change_memory(pid, address, value):
    process_handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    ctypes.windll.kernel32.VirtualAllocEx(process_handle, address, 4, win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, address, ctypes.byref(ctypes.c_int(value)), 4, 0)
    win32api.CloseHandle(process_handle)

if __name__ == "__main__":
    process_name = "game.exe"
    pid = find_process_id(process_name)

    if pid:
        print(f"Process found: PID {pid}")
        memory_address = 0x12345678
        change_memory(pid, memory_address, 999)
        print("Memory value successfully changed!")
    else:
        print("Process not found!")
