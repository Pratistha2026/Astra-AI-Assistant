import speech_recognition as sr
from brain.command import process_command

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Say something...")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

print("🧠 Processing...")

text = r.recognize_google(audio)
print("You said:", text)

process_command(text)