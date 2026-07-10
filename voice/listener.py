import os
import time
import threading
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.5
recognizer.phrase_threshold = 0.3

MIN_THRESHOLD = 300
MAX_THRESHOLD = 4000
NOISE_MARGIN = 1.4

_cached_mic_index = "unset"


def list_microphones():
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"[{i}] {name}")


def _env_mic_index():
    raw = os.environ.get("ASTRA_MIC_INDEX")
    if raw is None or raw.strip() == "":
        return None
    try:
        return int(raw)
    except ValueError:
        print(f"ASTRA_MIC_INDEX='{raw}' is not a valid integer, ignoring it.")
        return None


def find_working_mic_index(force_refresh=False):
    global _cached_mic_index
    if not force_refresh and _cached_mic_index != "unset":
        return _cached_mic_index

    env_index = _env_mic_index()
    if env_index is not None:
        _cached_mic_index = env_index
        print(f"Using microphone index {env_index} (from ASTRA_MIC_INDEX).")
        return env_index

    try:
        with sr.Microphone(device_index=None):
            pass
        _cached_mic_index = None
        print("Using system default microphone.")
        return None
    except Exception:
        pass

    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        try:
            with sr.Microphone(device_index=i):
                pass
            _cached_mic_index = i
            print(f"Default mic unavailable, using [{i}] {name}.")
            return i
        except Exception:
            continue

    print("No usable microphone found.")
    _cached_mic_index = None
    return None


def _calibrate(source, duration):
    recognizer.adjust_for_ambient_noise(source, duration=duration)
    scaled = recognizer.energy_threshold * NOISE_MARGIN
    recognizer.energy_threshold = max(MIN_THRESHOLD, min(scaled, MAX_THRESHOLD))
    print(f"energy_threshold set to {recognizer.energy_threshold:.0f}")


def test_microphone(index, duration=3):
    try:
        with sr.Microphone(device_index=index) as source:
            print(f"Testing mic [{index}] - stay quiet for a sec...")
            _calibrate(source, duration=1.5)
            print("Now say something...")
            audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            print(f"[{index}] picked up audio, looks good")
            return True
    except sr.WaitTimeoutError:
        print(f"[{index}] nothing detected, probably not your mic")
        return False
    except Exception as e:
        print(f"[{index}] failed: {e}")
        return False


def _listen_once(mic_index, timeout, phrase_time_limit, calibration_duration, result):
    try:
        with sr.Microphone(device_index=mic_index) as source:
            _calibrate(source, duration=calibration_duration)
            print("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        result["text"] = text.lower().strip()
    except Exception as e:
        result["error"] = e


def listen(timeout=8, phrase_time_limit=12, retries=2, stop_event=None):
    mic_index = find_working_mic_index()

    for attempt in range(retries + 1):
        if stop_event is not None and stop_event.is_set():
            return None

        calibration_duration = 1.5 if attempt == 0 else 2.5

        result = {"text": None, "error": None}
        worker = threading.Thread(
            target=_listen_once,
            args=(mic_index, timeout, phrase_time_limit, calibration_duration, result),
            daemon=True,
        )
        worker.start()

        while worker.is_alive():
            if stop_event is not None and stop_event.is_set():
                return None
            worker.join(timeout=0.1)

        err = result["error"]

        if err is None:
            print("You said:", result["text"])
            return result["text"]

        if isinstance(err, sr.WaitTimeoutError):
            print("Listening timed out - no speech detected.")
            if attempt < retries:
                continue
            return None

        if isinstance(err, sr.UnknownValueError):
            print("Heard audio but couldn't understand it.")
            if attempt < retries:
                continue
            return None

        if isinstance(err, sr.RequestError):
            print(f"Speech service error: {err} (check your internet connection).")
            return None

        if isinstance(err, OSError):
            print(f"Microphone error: {err}")
            find_working_mic_index(force_refresh=True)
            if attempt < retries:
                time.sleep(0.3)
                continue
            return None

        print(f"Voice error: {err}")
        return None

    return None


if __name__ == "__main__":
    list_microphones()
    choice = input("Enter a mic index to test (or press Enter for default): ").strip()
    index = int(choice) if choice else None
    test_microphone(index)