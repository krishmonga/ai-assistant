import os
import pyautogui
import webbrowser
import pyttsx3
from time import sleep

# Initialize the speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # 0 for male, 1 for female
engine.setProperty("rate", 170)  # Adjust speech rate

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
        webbrowser.open(f"https://{query}")
        speak(f"Opening {query}.")
    else:
        # Handle local applications
        for app in dictapp:
            if app in query:
                os.system(f"start {dictapp[app]}")
                speak(f"{app} has been launched.")
                return
        # Handle unknown commands
        speak("Sorry, I couldn't find the application.")

def closeapp(query):
    """Close tabs or applications."""
    speak("Closing, sir.")
    query = query.lower()

    # Handle closing browser tabs
    if "tab" in query:
        try:
            # Extract the number of tabs to close from the query
            number_of_tabs = int([word for word in query.split() if word.isdigit()][0])
            for _ in range(number_of_tabs):
                pyautogui.hotkey("ctrl", "w")
                sleep(0.5)
            speak(f"Closed {number_of_tabs} tab(s).")
        except (IndexError, ValueError):
            speak("Please specify the number of tabs to close.")
        return
    
    # Handle closing applications
    for app in dictapp:
        if app in query:
            os.system(f"TASKKILL /F /IM {dictapp[app]}.exe")
            speak(f"{app} has been closed.")
            return
    
    # Handle unknown commands
    speak("Sorry, I couldn't find the application to close.")

# Example Usage
if __name__ == "__main__":
    while True:
        speak("How can I assist you?")
        query = input("Enter your command: ").strip()  # Simulating voice input with text input
        
        if "open" in query:
            openwebapp(query)
        elif "close" in query:
            closeapp(query)
        elif "exit" in query or "quit" in query:
            speak("Goodbye, sir. Have a great day!")
            break
        else:
            speak("I didn't understand that. Could you please repeat?")
