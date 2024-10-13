import pyttsx3
import datetime

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")  
    speak("I am your virtual assistant. How can I help you?")

if __name__ == "__main__":
    greetme()