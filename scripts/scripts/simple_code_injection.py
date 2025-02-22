import ctypes
import time
import psutil
import win32api

def find_pid(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return proc.info['pid']
    return None

def inject_code(pid, memory_address, new_value):
    process_handle = win32api.OpenProcess(0x1F0FFF, False, pid)
    ctypes.windll.kernel32.VirtualAllocEx(process_handle, memory_address, 4, 0x1000, 0x04)
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, memory_address, ctypes.byref(ctypes.c_int(new_value)), 4, 0)
    win32api.CloseHandle(process_handle)

if __name__ == "__main__":
    pid = find_pid("game.exe")  # Replace with the actual game process name
    if pid:
        print(f"PID found: {pid}")
        memory_address = 0x00123456  # Replace with the actual memory address
        inject_code(pid, memory_address, 999)  # Injecting new value into memory
        print("Memory value modified!")
    else:
        print("Game not found.")
