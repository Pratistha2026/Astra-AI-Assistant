# Astra AI Assistant

A desktop voice/text assistant built with Python and CustomTkinter. Type or speak a command and Astra will open apps, search the web, answer questions using Gemini, and talk back.

## Features

- Text or voice input (mic button)
- Opens installed apps and common websites by name
- Google search by voice/text
- Tells the current time
- Answers general questions using Google Gemini, with simple kid-friendly explanations
- Speaks replies out loud (pyttsx3, works offline)
- Reply mode switch in the sidebar: Text + Voice, or Text only
- Say/type "stop" (or tap the Stop button) to cut off speech and cancel whatever's running, instantly
- Say/type "exit" or "quit" to close the app

## Setup

1. Install Python 3.10+.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Get a Gemini API key from https://aistudio.google.com/app/apikey and put it in `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```
4. Run it:
   ```
   python app.py
   ```

Voice input needs a working microphone and `PyAudio`. On Windows, if `pip install pyaudio` fails, grab a prebuilt wheel matching your Python version instead.

## Project structure

```
app.py                  entry point
gui/main_window.py      the whole UI (CustomTkinter)
voice/speaker.py        text-to-speech (pyttsx3)
voice/listener.py       microphone input (SpeechRecognition)
brain/ai_brain.py       Gemini API calls + Astra's answer style
automation/app_opener.py    opens installed apps by name
automation/web_opener.py    opens websites by name
automation/search_engine.py Google search
```

## Adding apps or websites

`automation/app_opener.py` and `automation/web_opener.py` just contain name -> command/URL dictionaries. Add an entry there if you want Astra to recognize a new app or site.

## Notes

- Voice replies are split sentence by sentence so "stop" interrupts almost immediately instead of waiting for the whole reply to finish.
- Don't commit your `.env` file / API key to a public repo.