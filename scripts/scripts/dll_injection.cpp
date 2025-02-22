#include <Windows.h>
#include <iostream>
#include <string>

BOOL InjectDLL(DWORD dwProcessId, const char* dllPath) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwProcessId);
    if (hProcess == NULL) {
        std::cerr << "Error opening process!" << std::endl;
        return FALSE;
    }

    LPVOID pDllPath = VirtualAllocEx(hProcess, NULL, strlen(dllPath) + 1, MEM_COMMIT, PAGE_READWRITE);
    WriteProcessMemory(hProcess, pDllPath, dllPath, strlen(dllPath) + 1, NULL);

    HMODULE hKernel32 = GetModuleHandleA("kernel32.dll");
    FARPROC pLoadLibrary = GetProcAddress(hKernel32, "LoadLibraryA");

    CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)pLoadLibrary, pDllPath, 0, NULL);
    CloseHandle(hProcess);
    return TRUE;
}

int main() {
    DWORD dwProcessId = 1234;  
    const char* dllPath = "C:\\path\\to\\your\\cheat.dll"; 

    if (InjectDLL(dwProcessId, dllPath)) {
        std::cout << "DLL injected successfully!" << std::endl;
    } else {
        std::cout << "Failed to inject DLL." << std::endl;
    }

    return 0;
}
