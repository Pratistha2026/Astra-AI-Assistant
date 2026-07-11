# Astra AI Assistant

A desktop AI assistant for Windows that combines **voice interaction**, **desktop automation**, and **Google Gemini** to provide a natural AI-powered experience.

Users can interact using voice or text, ask questions, launch desktop applications, open websites, perform Google searches, and receive spoken responses through an intuitive desktop interface.

---

## Screenshot

![Astra Main Window](assets/main%20window.png)

---

## Demo

🎥 **Watch Astra in action**

https://github.com/Pratistha2026/Astra-AI-Assistant/blob/main/assets/Astra_Demo.mp4

---

## Features

* 🎙️ Voice and text command support
* 🤖 AI-powered responses using Google Gemini
* 🖥️ Launch installed Windows applications
* 🌐 Open popular websites (YouTube, Gmail, Google Maps, etc.)
* 🔎 Perform Google searches directly from Astra
* 🕒 Get the current system time
* 🔊 Offline text-to-speech using `pyttsx3`
* ⏹️ Interrupt speech playback with **Stop**
* 🚪 Exit the assistant using a voice or text command
* 🔄 Toggle between:

  * Voice + Text responses
  * Text-only responses

---

## Tech Stack

| Technology         | Purpose                          |
| ------------------ | --------------------------------- |
| Python              | Core application                 |
| CustomTkinter        | Desktop user interface           |
| Google Gemini API    | AI responses (via backend)       |
| SpeechRecognition   | Voice recognition                |
| PyAudio             | Microphone input                 |
| pyttsx3             | Offline text-to-speech           |
| requests            | Talking to the Astra backend     |
| Flask (backend only) | Hosts the AI endpoint remotely   |

---

## How AI Responses Work

Astra doesn't call Google Gemini directly from the desktop app. Instead, it
sends each question to a small hosted backend
(see [`astra-backend/`](astra-backend)), which holds the Gemini API key
securely and returns the answer. This means:

* You can download and run Astra with **no API key setup of your own**.
* No `.env` file or API key prompt is needed on first launch.
* The backend applies a light rate limit per user to keep things fair.

---

## Requirements

* Python 3.10 or newer
* Windows 10/11
* Working microphone (for voice commands)
* Internet connection (for AI responses)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Pratistha2026/Astra-AI-Assistant.git

cd Astra-AI-Assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

That's it — no API key setup needed. Astra talks to a hosted backend that
handles the AI responses for you.

---

## Project Structure

```text
Astra-AI-Assistant/

├── automation/
│   ├── app_opener.py
│   ├── search_engine.py
│   └── web_opener.py
│
├── assets/
│   ├── main window.png
│   └── Astra_Demo.mp4
│
├── brain/
│   ├── ai_brain.py
│   └── command.py
│
├── gui/
│   └── main_window.py
│
├── voice/
│   ├── listener.py
│   └── speaker.py
│
├── app.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Example Commands

```text
Open YouTube

Open Google

Search Python tutorials

What time is it?

Explain machine learning

Stop

Exit
```

---

## Notes

* Voice commands require a working microphone.
* Desktop application launching currently supports Windows.
* AI responses depend on the Astra backend being online; if it's
  unreachable, Astra will let you know instead of crashing.

---

## Future Improvements

* Conversation history
* Wake-word activation
* Additional desktop automation
* Cross-platform support (Linux/macOS)
* More built-in commands

---

## License

This project is licensed under the MIT License.

See the **LICENSE** file for details.

---

## Author

**Pratistha Singh**

GitHub: https://github.com/Pratistha2026