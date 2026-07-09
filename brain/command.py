from voice.speaker import speak
import webbrowser
import os

# 🌐 Web apps (safe + common)
WEB_APPS = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "gmail": "https://mail.google.com",
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "whatsapp web": "https://web.whatsapp.com",
    "github": "https://github.com",
    "chatgpt": "https://chat.openai.com",
    "twitter": "https://x.com",
    "linkedin": "https://linkedin.com",
    "maps": "https://maps.google.com",
    "drive": "https://drive.google.com",
    "netflix": "https://netflix.com",
    "spotify web": "https://open.spotify.com",
    "play store": "https://play.google.com/store"
}

# 💻 Local apps (Windows examples)
LOCAL_APPS = {
    "notepad": "notepad",
    "calculator": "calc",
    "cmd": "cmd",
    "paint": "mspaint"
}

def process_command(text):
    text = text.lower()

    # 🌐 Open websites/apps
    for app in WEB_APPS:
        if app in text:
            speak(f"Opening {app}")
            webbrowser.open(WEB_APPS[app])
            return

    # 💻 Open system apps
    for app in LOCAL_APPS:
        if app in text:
            speak(f"Opening {app}")
            os.system(LOCAL_APPS[app])
            return

    # 💬 basic chat responses
    if "hello" in text:
        speak("Hello, I am Astra your AI assistant")

    elif "your name" in text:
        speak("My name is Astra")

    elif "time" in text:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "date" in text:
        from datetime import datetime
        today = datetime.now().strftime("%A %d %B %Y")
        speak(f"Today is {today}")

    else:
        speak("I did not understand that command")