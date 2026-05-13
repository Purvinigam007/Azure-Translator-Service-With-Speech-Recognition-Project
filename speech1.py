import tkinter as tk
import requests
import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3

# 🔑 KEYS
speech_key = "Your Key"
speech_region = "Your Region"

translator_key = "Your Key"
translator_endpoint = "https://api.cognitive.microsofttranslator.com/"
region = "Your Region"

# 🎤 RECORD AUDIO
def record_audio():
    duration = 5  # seconds
    fs = 44100
    status_label.config(text="🎤 Recording...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    write("voice.wav", fs, recording)
    status_label.config(text="✅ Recording Done")

# 🧠 SPEECH TO TEXT (Azure)
def speech_to_text():
    url = f"https://{speech_region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US"

    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type": "audio/wav"
    }

    with open("voice.wav", "rb") as f:
        response = requests.post(url, headers=headers, data=f)

    result = response.json()

    try:
        text = result["DisplayText"]
    except:
        text = "Speech not recognized"

    input_text.delete(0, tk.END)
    input_text.insert(0, text)

# 🌐 TRANSLATE
def translate():
    text = input_text.get()

    url = translator_endpoint + "translate?api-version=3.0&to=hi"

    headers = {
        "Ocp-Apim-Subscription-Key": translator_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json"
    }

    body = [{"text": text}]
    res = requests.post(url, headers=headers, json=body).json()

    try:
        translated = res[0]["translations"][0]["text"]
    except:
        translated = "Translation error"

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, translated)

    speak(translated)

# 🔊 TEXT TO SPEECH
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 🎨 UI
root = tk.Tk()
root.title("🎤 Speech Translator AI")
root.geometry("600x600")
root.config(bg="#0f172a")

title = tk.Label(root, text="🎤 Speech Translator AI", font=("Arial", 18, "bold"),
                 bg="#0f172a", fg="white")
title.pack(pady=10)

input_text = tk.Entry(root, width=40, font=("Arial", 14))
input_text.pack(pady=10)

record_btn = tk.Button(root, text="🎤 Record Voice", command=record_audio,
                       bg="#3b82f6", fg="white", width=20)
record_btn.pack(pady=5)

convert_btn = tk.Button(root, text="🧠 Speech to Text", command=speech_to_text,
                        bg="#22c55e", fg="white", width=20)
convert_btn.pack(pady=5)

translate_btn = tk.Button(root, text="🌐 Translate & Speak", command=translate,
                          bg="#f59e0b", fg="white", width=20)
translate_btn.pack(pady=5)

status_label = tk.Label(root, text="", bg="#0f172a", fg="white")
status_label.pack(pady=5)

output_text = tk.Text(root, height=10, width=50, bg="#1e293b", fg="white")
output_text.pack(pady=10)

root.mainloop()