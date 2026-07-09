import os

apps = {
    # Browsers
    "chrome": "start chrome",
    "google chrome": "start chrome",
    "edge": "start msedge",
    "microsoft edge": "start msedge",
    "firefox": "start firefox",

    # Windows common apps
    "file explorer": "explorer",
    "files": "explorer",
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "gallery": "start ms-photos:",
    "photos": "start ms-photos:",
    "camera": "start microsoft.windows.camera:",
    "settings": "start ms-settings:",
    "control panel": "control",
    "task manager": "taskmgr",
    "command prompt": "cmd",
    "terminal": "wt",
    "powershell": "powershell",

    # Microsoft apps
    "word": "start winword",
    "excel": "start excel",
    "powerpoint": "start powerpnt",
    "outlook": "start outlook",
    "onenote": "start onenote",

    # Developer tools
    "vs code": "code",
    "visual studio code": "code",
    "python": "python",

    # Media / Communication
    "spotify": "start spotify",
    "media player": "start wmplayer",
    "whatsapp": "start whatsapp:",
    "zoom": "start zoommtg:",
}

# Maps app name -> the actual process (.exe) name Windows uses
process_names = {
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "firefox": "firefox.exe",
    "file explorer": "explorer.exe",
    "files": "explorer.exe",
    "notepad": "notepad.exe",
    "calculator": "CalculatorApp.exe",
    "paint": "mspaint.exe",
    "settings": "SystemSettings.exe",
    "control panel": "control.exe",
    "task manager": "Taskmgr.exe",
    "command prompt": "cmd.exe",
    "terminal": "WindowsTerminal.exe",
    "powershell": "powershell.exe",
    "word": "WINWORD.EXE",
    "excel": "EXCEL.EXE",
    "powerpoint": "POWERPNT.EXE",
    "outlook": "OUTLOOK.EXE",
    "onenote": "ONENOTE.EXE",
    "vs code": "Code.exe",
    "visual studio code": "Code.exe",
    "spotify": "Spotify.exe",
    "media player": "wmplayer.exe",
    "whatsapp": "WhatsApp.exe",
    "zoom": "Zoom.exe",
}


def open_app(app_name):
    app_name = app_name.lower().strip()
    if app_name in apps:
        os.system(apps[app_name])
        return True
    return False


def close_app(app_name):
    app_name = app_name.lower().strip()
    if app_name in process_names:
        os.system(f"taskkill /f /im {process_names[app_name]}")
        return True
    return False