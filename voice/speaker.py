"""
voice/speaker.py
Text-to-speech for Astra, using pyttsx3 (offline).
"""

import pyttsx3
import threading
import re

_lock = threading.Lock()
_active_engine = None
_stop_flag = threading.Event()

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")

PREFERRED_VOICES = ["zira", "female", "hazel", "susan", "samantha"]


def _pick_voice(engine):
    voices = engine.getProperty("voices")
    if not voices:
        return None

    for keyword in PREFERRED_VOICES:
        for v in voices:
            name = (v.name or "").lower()
            if keyword in name:
                return v.id

    return voices[1].id if len(voices) > 1 else voices[0].id


def speak(text):
    global _active_engine

    if not text:
        return

    _stop_flag.clear()

    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text.strip()) if s.strip()]
    if not sentences:
        sentences = [text.strip()]

    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
    engine.setProperty("volume", 1.0)

    voice_id = _pick_voice(engine)
    if voice_id:
        engine.setProperty("voice", voice_id)

    with _lock:
        _active_engine = engine

    try:
        for sentence in sentences:
            if _stop_flag.is_set():
                break

            print("[ASTRA SAYS]", sentence)

            try:
                engine.say(sentence)
                engine.runAndWait()
            except RuntimeError:
                break

            if _stop_flag.is_set():
                break
    finally:
        try:
            engine.stop()
        except Exception:
            pass
        with _lock:
            _active_engine = None


def stop_speaking():
    _stop_flag.set()
    with _lock:
        engine = _active_engine
    if engine is not None:
        try:
            engine.stop()
        except Exception:
            pass


def list_available_voices():
    engine = pyttsx3.init()
    for v in engine.getProperty("voices"):
        print(v.id, "-", v.name)
    engine.stop()


if __name__ == "__main__":
    list_available_voices()
    speak("Hello, this is Astra. How can I help you today?")