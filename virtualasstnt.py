import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=4)
        except Exception as e:
            speak("Sorry, I couldn't hear that. Please repeat.")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    
    return query.lower()

def get_temperature(query):
    search = "temperature in " + query.replace("temperature", "").strip()
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    try:
        temp = data.find("div", class_="BNeawe").text
        speak(f"The current {search} is {temp}")
    except Exception as e:
        speak("Sorry, I couldn't fetch the temperature. Please try again later.")

def start_jarvis():
    speak("Hello, I am your virtual assistant. How can I help you?")

def stop_jarvis():
    speak("Okay, you can call me anytime.")
    return "sleep"

if __name__ == "__main__":
    jarvis_active = True  # To track if Jarvis is active or sleeping

    while True:
        if jarvis_active:
            query = takeCommand()

            if "wake up" in query:
                start_jarvis()
            
            if "go to sleep" in query:
                jarvis_active = False
                stop_jarvis()
                continue
            
            elif "hello" in query:
                speak("Hello sir, how can I help you?")
            elif "i am sorry" in query:
                speak("I did not get that. Please repeat.")
            elif "thank you" in query:
                speak("You are welcome sir.")
            elif "open" in query:
                from dictapp import openwebapp
                openwebapp(query)
            elif "close" in query:
                from dictapp import closeapp
                closeapp(query)
            elif "google" in query:
                from searchnow import searchGoogle
                searchGoogle(query)
            elif "youtube" in query:
                from searchnow import searchyoutube
                searchyoutube(query)
            elif "wikipedia" in query:
                from searchnow import searchwikipedia
                searchwikipedia(query)
            elif "whatsapp" in query:
                pass
            elif "temperature" in query or "weather" in query:
                get_temperature(query)
        
        # Waiting for "wake up" when Jarvis is in sleep mode
        else:
            query = takeCommand()
            if "wake up" in query:
                jarvis_active = True
                start_jarvis()
            elif "finally sleep" in query:
                speak("Going to sleep. Goodbye!")
                break  # Exit the loop and stop the assistant
8