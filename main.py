# Nosso main file

"""
Teste de Reconhecimento

import speech_recognition as sr

# cria um reconhecedor
r = sr.Recognizer()

# abrir microfone para captura
with sr.Microphone() as source:
    while True:
        audio = r.listen(source) # define microfone como fonte de audio
    
        print(r.recognize_google(audio, language='pt'))

"""

#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import json
import pyaudio
import pyttsx3
import core 
from nlu.classifire import classify
import psutil, os

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()



def evaluate(text):
    # reconhecer entidade do texto
    entity = classify(text)
        
        
    if entity == 'time|getTime':
            speak(core.SystemInfo.get_time())
    elif entity == 'time|getDate':
            speak(core.SystemInfo.get_date())

    # Perguntas à tulip
    elif entity == 'question|getName':
        speak('Meu nome é Tulípa')  

    # abrir programas

    elif entity == 'open|notepad':
        speak('Abrindo bloco de notas')
        os.system('notepad.exe')

    elif entity == 'open|chrome':
        speak('Abrindo google chrome')

        os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe"')

            
    elif entity == 'open|vivaldi':
        speak('Abrindo vivaldi')
        os.system('C:/Users/user/AppData/Local/Vivaldi/Application/vivaldi.exe')

    print(f'Text: {text} Entity: {entity}')


# reconhecimento de fala

# Sintese de fala
model = Model("model")
rec = KaldiRecognizer(model, 16000)

CHUNK = 256

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=CHUNK)
stream.start_stream()

# loop do reconhecimento de fala
while True:
        data = stream.read(CHUNK)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result = json.loads(result)

            if result is not None:
                text = result['text']
                evaluate(text)
                