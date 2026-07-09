# Astra AI Assistant

Astra is a desktop AI assistant built with Python that accepts both voice and text commands. It can open applications, search the web, answer questions using Google Gemini, and respond using text-to-speech through a simple desktop interface.

I built this project to explore how speech recognition, desktop automation, and generative AI can work together in a single application.

---

## Features

- Voice and text input
- AI-powered responses using Google Gemini
- Open installed desktop applications
- Open websites such as YouTube and Google
- Search Google directly from Astra
- Current time information
- Offline text-to-speech using pyttsx3
- Stop command to interrupt speech immediately
- Switch between **Text + Voice** and **Text Only** reply modes
- Exit command to close the application

---

## Technologies Used

- Python
- CustomTkinter
- Google Gemini API
- SpeechRecognition
- PyAudio
- pyttsx3
- python-dotenv

---

## Installation

Clone the repository.

```bash
git clone https://github.com/Pratistha2026/Astra-AI-Assistant.git
```

Move into the project folder.

```bash
cd Astra-AI-Assistant
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application.

```bash
python app.py
```

---

## Project Structure

```text
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

Storage/

app.py
requirements.txt
README.md
```

---

## Example Commands

- Open YouTube
- Open Google
- Search Python tutorials
- What time is it?
- Explain machine learning
- Stop
- Exit

---

## Notes

- A valid Google Gemini API key is required.
- Voice input requires a working microphone.
- Never upload your `.env` file or API key.
- If PyAudio installation fails on Windows, install a compatible prebuilt wheel for your Python version.

---

## Author

**Pratistha Singh**

GitHub: https://github.com/Pratistha2026