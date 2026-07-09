# Astra AI Assistant

Astra is a desktop AI assistant that I built using Python. It accepts both voice and text commands and can perform everyday tasks such as opening applications, searching the web, answering questions with Google Gemini, and responding through speech.

The goal of this project was to combine speech recognition, desktop automation, and generative AI into a single application with a simple user interface.

---

## Features

- Voice and text input
- AI responses using Google Gemini
- Opens installed desktop applications
- Opens websites like YouTube and Google
- Google search
- Speaks responses using text-to-speech
- Displays the current time
- Stop command to interrupt speech
- Option to switch between voice responses and text-only responses
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

Install the required packages.

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project folder.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application.

```bash
python app.py
```

---

## Project Structure

```
automation/      Handles application launching, website opening and Google search
brain/           AI response generation and command processing
gui/             CustomTkinter interface
voice/           Speech recognition and text-to-speech
Storage/         Stores project data
app.py           Main entry point
```

---

## Example Commands

- Open YouTube
- Open Chrome
- Search Python tutorials
- What time is it?
- Explain machine learning
- Stop
- Exit

---

## Notes

- A valid Google Gemini API key is required.
- Voice input requires a working microphone.
- Do not upload your `.env` file or API key.

---

## Author

Pratistha Singh

GitHub: https://github.com/Pratistha2026