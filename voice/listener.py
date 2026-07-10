import os
import threading
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 150
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.5

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


def test_microphone(index, duration=3):
    try:
        with sr.Microphone(device_index=index) as source:
            print(f"Testing mic [{index}] - stay quiet for a sec...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
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


def _listen_interruptible(source, timeout, phrase_time_limit, stop_event):
    if stop_event is None:
        return recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    result = {"audio": None, "error": None}

    def _worker():
        try:
            result["audio"] = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except Exception as e:
            result["error"] = e

    worker = threading.Thread(target=_worker, daemon=True)
    worker.start()

    while worker.is_alive():
        if stop_event.is_set():
            return None
        worker.join(timeout=0.1)

    if result["error"] is not None:
        raise result["error"]
    return result["audio"]


def listen(timeout=8, phrase_time_limit=10, retries=1, stop_event=None):
    mic_index = find_working_mic_index()

    for attempt in range(retries + 1):
        if stop_event is not None and stop_event.is_set():
            return None
        try:
            with sr.Microphone(device_index=mic_index) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1.2)
                if stop_event is not None and stop_event.is_set():
                    return None
                print("Listening...")
                audio = _listen_interruptible(source, timeout, phrase_time_limit, stop_event)

            if audio is None:
                return None

            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            text = text.lower().strip()
            print("You said:", text)
            return text

        except sr.WaitTimeoutError:
            print("Listening timed out - no speech detected.")
            if attempt < retries and not (stop_event is not None and stop_event.is_set()):
                continue
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            return None
        except OSError as e:
            print(f"Microphone error: {e}")
            find_working_mic_index(force_refresh=True)
            return None

    return None


if __name__ == "__main__":
    list_microphones()
    choice = input("Enter a mic index to test (or press Enter for default): ").strip()
    index = int(choice) if choice else None
    test_microphone(index)