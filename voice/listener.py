import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 150
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.5

MIC_INDEX = 22


def list_microphones():
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"[{i}] {name}")


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


def listen(timeout=8, phrase_time_limit=10, retries=1):
    for attempt in range(retries + 1):
        try:
            with sr.Microphone(device_index=MIC_INDEX) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1.2)
                print("Listening...")
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            text = text.lower().strip()
            print("You said:", text)
            return text

        except sr.WaitTimeoutError:
            print("Listening timed out - no speech detected.")
            if attempt < retries:
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
            return None

    return None


if __name__ == "__main__":
    list_microphones()
    choice = input("Enter a mic index to test (or press Enter for default): ").strip()
    index = int(choice) if choice else None
    test_microphone(index)