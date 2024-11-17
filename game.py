import os 
import pyautogui
import webbrowser
import pyttsx3
from time import sleep

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)   

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

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
    speak("Launching, sir.")
    query = query.lower().replace("open", "").replace("jarvis", "").replace("launch", "").strip()
    
    if any(ext in query for ext in [".com", ".co.in", ".org"]):
        webbrowser.open(f"https://www.{query}")
    else:
        for app in dictapp.keys():
            if app in query:
                os.system(f"start {dictapp.get(app)}")
                break
                
def closeapp(query):
    speak("Closing, sir.")
    if "one tab" in query or "1 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed.")
    elif "two tab" in query or "2 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed.")
    elif "three tab" in query or "3 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed.")
    elif "four tab" in query or "4 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed.")
    elif "five tab" in query or "5 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed.")
    else:
        keys = list(dictapp.keys())
        for app in keys:
            if app in query:
                os.system(f"TASKKILL /F /IM {dictapp.get(app)}.exe")
