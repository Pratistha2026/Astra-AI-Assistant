# Astra AI Assistant

A desktop AI assistant for Windows that accepts voice and text commands, answers questions using Google Gemini, and automates common desktop tasks like opening apps and searching the web.

Built to explore how speech recognition, desktop automation, and generative AI fit together in a single application.

![Astra main window](assets/main%20window.png)

## Features

- Voice and text input, with a toggle between Text + Voice and Text Only reply modes
- AI-powered answers via Google Gemini
- Opens installed desktop applications (Windows only)
- Opens websites such as YouTube, Gmail, and Google Maps
- Runs Google searches directly from Astra
- Reports the current time
- Offline text-to-speech (pyttsx3), interruptible with a stop command
- Exit command to close the app

## Tech Stack

- Python
- CustomTkinter — desktop UI
- Google Gemini API — AI responses
- SpeechRecognition + PyAudio — voice input
- pyttsx3 — offline text-to-speech
- python-dotenv — environment config

## Getting Started

**1. Clone the repo**

```bash
git clone https://github.com/Pratistha2026/Astra-AI-Assistant.git
cd Astra-AI-Assistant
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure your API key**

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

**4. Run it**

```bash
python app.py
```

## Project Structure

```
automation/
    app_opener.py
    search_engine.py
    web_opener.py

brain/
    ai_brain.py
    command.py

gui/
    main_window.py

voice/
    listener.py
    speaker.py

assets/
    main window.png
    Astra_Demo.mp4

app.py
requirements.txt
```

## Example Commands

```
Open YouTube
Open Google
Search Python tutorials
What time is it?
Explain machine learning
Stop
Exit
```

## Notes

- Requires a valid Gemini API key.
- Voice input requires a working microphone.
- Desktop app launching (Notepad, Calculator, etc.) is Windows-only.
- Do not commit your `.env` file or API key.
- If `PyAudio` fails to install on Windows, grab a prebuilt wheel matching your Python version.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Pratistha Singh**
[github.com/Pratistha2026](https://github.com/Pratistha2026)