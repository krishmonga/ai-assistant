import googletrans
from googletrans import Translator  # pip install googletrans==4.0.0-rc1
from gtts import gTTS  # pip install gtts
import pyttsx3
import speech_recognition as sr
import os
from playsound import playsound  # pip install playsound==1.2.2
import time

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, timeout=4)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def translategl(query):
    speak("Sure, sir.")
    print("Available languages:")
    print(googletrans.LANGUAGES)  # Displays supported languages
    translator = Translator()

    speak("Choose the language code for translation from the above list.")
    b = input("To_Lang (Enter language code, e.g., 'hi' for Hindi):- ")   

    try:
        # Translate text
        text_to_translate = translator.translate(query, src="auto", dest=b)
        text = text_to_translate.text
        print(f"Translated Text: {text}")

        # Use gTTS for text-to-speech
        speakgl = gTTS(text=text, lang=b, slow=False)
        speakgl.save("voice.mp3")
        playsound("voice.mp3")
        
        # Clean up the temporary audio file
        time.sleep(1)
        os.remove("voice.mp3")
    except Exception as e:
        print("Unable to translate or play the translated text.")
        print(f"Error: {e}")
        speak("Sorry, I could not translate the text.")

# Example usage
if __name__ == "__main__":
    speak("Please say something to translate.")
    query = takeCommand()
    if query != "None":
        translategl(query)
