import speech_recognition as sr

recognizer = sr.Recognizer()


def scan_all_mics():
    names = sr.Microphone.list_microphone_names()
    working = []

    for i, name in enumerate(names):
        try:
            with sr.Microphone(device_index=i) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print(f"[{i}] OK   - {name}")
            working.append(i)
        except Exception as e:
            print(f"[{i}] FAIL - {name} ({e})")

    print("\nWorking mic indices:", working)


if __name__ == "__main__":
    scan_all_mics()