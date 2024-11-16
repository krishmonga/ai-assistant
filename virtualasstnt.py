import os
import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

for i in range(3):
    a = input("Enter Password to open Jarvis :- ")
    pw_file = open("password.txt", "r")
    pw = pw_file.read()
    pw_file.close()
    if a == pw:
        from INTRO import play_gif
        play_gif()
        print("WELCOME SIR ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
        break
    elif i == 2 and a != pw:
        exit()
    elif a != pw:
        print("Try Again")

def change_password(query):
    if "change password" in query:
        speak("What's the new password")
        new_pw = input("Enter the new password\n")
        new_password = open("password.txt", "w")
        new_password.write(new_pw)
        new_password.close()
        speak("Done sir")
        speak(f"Your new password is {new_pw}")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

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
            query = takeCommand().lower()

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
            elif "screenshot" in query:
                import pyautogui  # pip install pyautogui
                im = pyautogui.screenshot()
                im.save("ss.jpg")
                speak("Screenshot taken and saved as ss.jpg")
            elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")
            elif "translate" in query:
                    from Translator import translategl
                    query = query.replace("jarvis","")
                    query = query.replace("translate","")
                    translategl(query)
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
            elif "whatsapp" in query:
                from whatsapp import sendMessage
                sendMessage()
            elif "change password" in query:
                change_password(query)
            elif "play a game" in query:
                from game import game_play
                game_play()
        
        # Waiting for "wake up" when Jarvis is in sleep mode
        else:
            query = takeCommand().lower()
            if "wake up" in query:
                jarvis_active = True
                start_jarvis()
            elif "finally sleep" in query:
                speak("Going to sleep. Goodbye!")
                break  # Exit the loop and stop the assistant
            elif "shutdown the system" in query:
                speak("Are You sure you want to shutdown")
                shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                if shutdown == "yes":
                    os.system("shutdown /s /t 1")
                    break
                elif shutdown == "no":
                    break
                else:
                    speak("I am in sleep mode. Wake me up if you need anything.")
                    continue