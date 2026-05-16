import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx4
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

engine = pyttsx4.init()
def say_to_me(talk):
    engine.say(talk)
    engine.runAndWait()

fs = 16000
seconds = 4
recognizer = sr.Recognizer()

print("Говори...")

while True:
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()

    audio_int16 = (audio * 32767).astype(np.int16)
    audio_data = sr.AudioData(audio_int16.tobytes(), fs, 2)

    try:
        text = recognizer.recognize_google(audio_data, language='en-US')
        text = text.lower()

        print("Почув:", text)

        if "write file" in text:
            img = Image.open("image.png")
            result = pytesseract.image_to_string(img,lang="ukr+eng")

            with open ('image_text.txt', 'w', encoding="utf-8") as f:
                f.write(result)
                say_to_me("записано у файл")

            say_to_me("записано у файл")
        elif "read file" in text:
            with open ('image_text.txt', 'r', encoding="utf-8") as f:
                data = f.read()
                say_to_me("прочитано файл")

            print(data)
            say_to_me("прочитано файл")
        elif "exit" in text:
            say_to_me("Exit")
            break


    except Exception as e:
        print("Помилка розпізнавання:", e)
