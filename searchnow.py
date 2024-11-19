import os
import pyautogui
import webbrowser
import pyttsx3
from time import sleep
import speech_recognition as sr  # For voice input

# Initialize the speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

# Text-to-speech function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Recognize voice input
def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you please repeat?")
            return "None"
        except sr.RequestError:
            speak("There seems to be an issue with the speech recognition service.")
            return "None"
        return query.lower()

# Dictionary of applications
dictapp = {
    "command prompt": "cmd",
    "paint": "mspaint",
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vs code": "code",
    "powerpoint": "powerpnt",
}

# Open applications or websites
def openwebapp(query):
    speak("Checking the application, sir.")
    query = query.lower().replace("open", "").replace("launch", "").strip()

    # Handle web URLs
    if any(ext in query for ext in [".com", ".co.in", ".org", ".net"]):
        webbrowser.open(f"https://{query}")
        speak(f"Opening {query}.")
        return

    # Handle local applications
    for app in dictapp.keys():
        if app in query:
            os.system(f"start {dictapp[app]}")
            speak(f"{app} has been launched.")
            return

    speak("Sorry, I couldn't find the application you're looking for.")

# Close applications or tabs
def closeapp(query):
    speak("Processing your request, sir.")
    query = query.lower()

    # Close browser tabs
    if "tab" in query:
        try:
            number_of_tabs = int([word for word in query.split() if word.isdigit()][0])
            for _ in range(number_of_tabs):
                pyautogui.hotkey("ctrl", "w")
                sleep(0.5)
            speak(f"Closed {number_of_tabs} tab(s).")
        except (IndexError, ValueError):
            speak("Please specify the number of tabs to close.")
        return

    # Close applications
    for app in dictapp.keys():
        if app in query:
            os.system(f"TASKKILL /F /IM {dictapp[app]}.exe")
            speak(f"{app} has been closed.")
            return

    speak("Sorry, I couldn't find the application you're looking to close.")

# Main interactive loop
if __name__ == "__main__":
    speak("Welcome, sir! I am your assistant.")
    while True:
        speak("How can I assist you?")
        query = takeCommand()  # Use voice input

        if "open" in query:
            openwebapp(query)
        elif "close" in query:
            closeapp(query)
        elif "exit" in query or "quit" in query:
            speak("Goodbye, sir. Have a great day!")
            break
        elif query != "None":
            speak("I didn't understand that. Could you please repeat?")
