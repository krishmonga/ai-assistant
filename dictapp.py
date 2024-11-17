import os
import pyautogui
import webbrowser
import pyttsx3
from time import sleep

# Initialize the speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(audio):
    """Text-to-speech function."""
    engine.say(audio)
    engine.runAndWait()

# Dictionary of applications
dictapp = {
    "commandprompt": "cmd",
    "paint": "mspaint",
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vscode": "code",
    "powerpoint": "powerpnt"
}

def openwebapp(query):
    """Open a web application or local application."""
    speak("Launching, sir.")
    query = query.lower().replace("open", "").replace("jarvis", "").replace("launch", "").strip()
    
    # Handle web URLs
    if any(ext in query for ext in [".com", ".co.in", ".org"]):
        webbrowser.open(f"https://www.{query}")
        return

    # Handle local applications
    for app in dictapp.keys():
        if app in query:
            os.system(f"start {dictapp[app]}")
            speak(f"{app} has been launched.")
            return
    
    # Handle unknown commands
    speak("Sorry, I couldn't find the application you're looking for.")

def closeapp(query):
    """Close tabs or applications."""
    query = query.lower()
    speak("Closing, sir.")
    
    # Close browser tabs
    if "tab" in query:
        try:
            # Extract the number of tabs from the query
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
    
    # Handle unknown commands
    speak("Sorry, I couldn't find the application you're looking to close.")

# Example Usage
if __name__ == "__main__":
    query = "open chrome"  # Example query
    openwebapp(query)

    query = "close 3 tabs"  # Example query
    closeapp(query)
