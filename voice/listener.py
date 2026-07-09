"""
voice/listener.py
Handles microphone input and converts speech to text using Google's
Speech Recognition API (via the `speech_recognition` library).
"""

import speech_recognition as sr

# One shared recognizer instance
recognizer = sr.Recognizer()

# Tuning these makes listening far more reliable in normal rooms
recognizer.energy_threshold = 300        # higher = ignores more background noise
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8         # how long a silence counts as "done talking"


def listen(timeout=5, phrase_time_limit=8):
    """
    Listens through the default microphone and returns the recognized
    text in lowercase, or None if nothing usable was heard.
    """
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            print("Listening...")
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        text = text.lower().strip()
        print("You said:", text)
        return text

    except sr.WaitTimeoutError:
        print("Listening timed out - no speech detected.")
        return None
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Speech service error: {e}")
        return None
    except OSError as e:
        print(f"Microphone error: {e}")
        return None