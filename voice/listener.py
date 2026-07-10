import os
import threading
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.dynamic_energy_ratio = 1.8
recognizer.pause_threshold = 0.8
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


def _listen_once(mic_index, timeout, phrase_time_limit, result):
    try:
        with sr.Microphone(device_index=mic_index) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1.5)
            # add headroom above the measured noise floor so steady
            # background noise (fan, traffic, chatter) doesn't trip
            # the recognizer into thinking it's speech
            recognizer.energy_threshold = max(recognizer.energy_threshold, 300) + 50
            print("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        result["text"] = text.lower().strip()
    except Exception as e:
        result["error"] = e


def listen(timeout=8, phrase_time_limit=10, retries=1, stop_event=None):
    mic_index = find_working_mic_index()

    for attempt in range(retries + 1):
        if stop_event is not None and stop_event.is_set():
            return None

        result = {"text": None, "error": None}
        worker = threading.Thread(target=_listen_once, args=(mic_index, timeout, phrase_time_limit, result), daemon=True)
        worker.start()

        while worker.is_alive():
            if stop_event is not None and stop_event.is_set():
                # We stop waiting so the UI is freed right away. The worker
                # thread still owns the mic stream and will close it itself
                # once its listen()/recognize() call finishes on its own.
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
            print("Could not understand the audio.")
            return None

        if isinstance(err, sr.RequestError):
            print(f"Speech service error: {err}")
            return None

        if isinstance(err, OSError):
            print(f"Microphone error: {err}")
            find_working_mic_index(force_refresh=True)
            return None

        print(f"Voice error: {err}")
        return None

    return None


if __name__ == "__main__":
    list_microphones()
    choice = input("Enter a mic index to test (or press Enter for default): ").strip()
    index = int(choice) if choice else None
    test_microphone(index)