import os
import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import webbrowser  # For opening websites like YouTube, Facebook
import subprocess  # For launching apps like Spotify or other installed programs
import pyautogui  # For taking screenshots

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Global variable for Jarvis activity
jarvis_active = True

# Function to speak responses
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to listen for voice commands
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except sr.UnknownValueError:
            speak("I didn't catch that. Please say it again.")
            return "None"
        except sr.RequestError:
            speak("Unable to connect to the speech recognition service.")
            return "None"
        return query.lower()

# Function to fetch the temperature
def get_temperature(command):
    try:
        location = command.replace("temperature", "").replace("weather", "").strip()
        if not location:
            speak("Please specify a location.")
            return
        url = f"https://www.google.com/search?q=temperature+in+{location}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        temperature = soup.find("div", class_="BNeawe").text
        speak(f"The current temperature in {location} is {temperature}.")
    except Exception as e:
        print(f"Error fetching temperature: {e}")
        speak("Sorry, I couldn't retrieve the temperature. Please try again later.")

# Function to execute system commands
def execute_system_command(command):
    if "shutdown" in command:
        speak("Are you sure you want to shut down?")
        if messagebox.askyesno("Shutdown", "Do you want to shut down the computer?"):
            os.system("shutdown /s /t 1")
        else:
            speak("Shutdown cancelled.")
    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif "log off" in command:
        speak("Logging off.")
        os.system("shutdown /l")

# Function to open common apps or websites
def open_app(command):
    if "notepad" in command:
        speak("Opening Notepad.")
        subprocess.run(["notepad"])
    elif "calculator" in command:
        speak("Opening Calculator.")
        subprocess.run(["calc"])
    elif "browser" in command:
        speak("Opening your default browser.")
        webbrowser.open("https://www.google.com")

# Function to take a screenshot
def take_screenshot():
    speak("Taking a screenshot.")
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken and saved as screenshot.png.")

# Function to process commands
def process_command(command):
    global jarvis_active
    if "wake up" in command:
        if not jarvis_active:
            speak("I am already active.")
        else:
            speak("I am awake and ready to assist you.")
            jarvis_active = True
    elif "go to sleep" in command:
        speak("Going to sleep. Say 'wake up' to activate me.")
        jarvis_active = False
    elif "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "thank you" in command:
        speak("You're welcome!")
    elif "temperature" in command or "weather" in command:
        get_temperature(command)
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in command:
        speak("Opening Facebook.")
        webbrowser.open("https://www.facebook.com")
    elif "play music" in command or "spotify" in command:
        speak("Opening Spotify.")
        try:
            subprocess.run(["spotify"])
        except FileNotFoundError:
            speak("Spotify is not installed.")
    elif "shutdown" in command or "restart" in command or "log off" in command:
        execute_system_command(command)
    elif "screenshot" in command:
        take_screenshot()
    elif "open notepad" in command or "open calculator" in command or "open browser" in command:
        open_app(command)
    elif "finally sleep" in command:
        speak("Shutting down. Goodbye!")
        root.quit()

# GUI interface
def gui_interface():
    def on_command_entry():
        if not jarvis_active:
            speak("I am currently asleep. Please wake me up first.")
            return
        command = command_entry.get()
        process_command(command)
        command_entry.delete(0, tk.END)

    def on_voice_command():
        if not jarvis_active:
            speak("I am currently asleep. Please wake me up first.")
            return
        command = takeCommand()
        if command != "None":
            process_command(command)

    global root
    root = tk.Tk()
    root.title("Virtual Assistant")

    # Instructions
    tk.Label(root, text="Enter or speak a command:", font=("Arial", 14)).pack(pady=10)

    # Command entry box
    command_entry = tk.Entry(root, font=("Arial", 14), width=40)
    command_entry.pack(pady=10)

    # Submit button
    tk.Button(root, text="Submit", font=("Arial", 12), command=on_command_entry).pack(pady=5)

    # Speak button
    tk.Button(root, text="Speak", font=("Arial", 12), command=on_voice_command).pack(pady=5)

    root.mainloop()

# Main execution
if __name__ == "__main__":
    print("Welcome! Say 'Wake up' to activate me.")
    gui_interface()
