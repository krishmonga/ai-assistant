import os
import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import webbrowser  # For opening websites like YouTube, Facebook
import subprocess  # For launching apps like Spotify

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Global variable to track Jarvis state
jarvis_active = True

# Function to speak the assistant's response
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
            print(f"User said: {query}")  # Debugging line
        except sr.UnknownValueError:
            print("Could not understand audio. Say that again, please...")
            return "None"
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return "None"
        return query

# Function to get the temperature
def get_temperature(query):
    try:
        search = "temperature in " + query.replace("temperature", "").strip()
        url = f"https://www.google.com/search?q={search}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(f"The current {search} is {temp}")
    except Exception as e:
        print(f"Error fetching temperature: {e}")
        speak("Sorry, I couldn't fetch the temperature. Please try again later.")

# Function to start Jarvis (assistant)
def start_jarvis():
    speak("Hello, I am your virtual assistant. How can I help you?")

# Function to stop Jarvis
def stop_jarvis():
    speak("Okay, you can call me anytime.")
    return "sleep"

# Function to open WhatsApp
def open_whatsapp():
    speak("Opening WhatsApp")
    webbrowser.open("https://web.whatsapp.com")
    os.system("start whatsapp")

# Function to open YouTube
def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

# Function to open Facebook
def open_facebook():
    speak("Opening Facebook")
    webbrowser.open("https://www.facebook.com")

# Function to play music on Spotify
def play_music():
    speak("Opening Spotify and playing music")
    try:
        subprocess.run(["spotify"])  # Ensure Spotify is installed and in your PATH
    except FileNotFoundError:
        speak("Spotify is not installed or not found in your system's PATH.")

# Function to process commands
def process_command(command):
    global jarvis_active
    command = command.lower()
    print(f"Processing command: {command}")  # Debugging line

    if "wake up" in command:
        print("Wake up command detected")  # Debugging line
        start_jarvis()
    elif "go to sleep" in command:
        print("Go to sleep command detected")  # Debugging line
        jarvis_active = False
        stop_jarvis()
    elif "hello" in command:
        print("Hello command detected")  # Debugging line
        speak("Hello sir, how can I help you?")
    elif "thank you" in command:
        print("Thank you command detected")  # Debugging line
        speak("You are welcome, sir.")
    elif "open youtube" in command:
        print("Opening YouTube...")  # Debugging line
        open_youtube()
    elif "open facebook" in command:
        print("Opening Facebook...")  # Debugging line
        open_facebook()
    elif "play music" in command or "spotify" in command:
        print("Opening Spotify and playing music...")  # Debugging line
        play_music()
    elif "temperature" in command or "weather" in command:
        print("Fetching temperature...")  # Debugging line
        get_temperature(command)
    elif "shutdown the system" in command:
        speak("Are you sure you want to shutdown?")
        shutdown = messagebox.askyesno("Shutdown", "Do you wish to shutdown your computer?")
        if shutdown:
            os.system("shutdown /s /t 1")
        else:
            speak("Shutdown cancelled.")
    elif "finally sleep" in command:
        print("Shutting down...")  # Debugging line
        speak("Going to sleep. Goodbye!")
        root.quit()
    elif "screenshot" in command:
        print("Taking screenshot...")  # Debugging line
        import pyautogui
        im = pyautogui.screenshot()
        im.save("ss.jpg")
        speak("Screenshot taken and saved as ss.jpg")

# GUI for interacting with the assistant
def gui_interface():
    global jarvis_active
    def on_command_entry():
        command = command_entry.get()  # Get text from command entry box
        process_command(command)
        command_entry.delete(0, tk.END)  # Clear the entry box

    def on_voice_command():
        command = takeCommand()  # Get command via voice
        if command != "None":
            process_command(command)

    # Creating the main window
    global root
    root = tk.Tk()
    root.title("Virtual Assistant")

    # Adding a label for instructions
    label = tk.Label(root, text="Enter or speak a command", font=("Arial", 14))
    label.pack(pady=10)

    # Adding a text entry box
    command_entry = tk.Entry(root, width=40, font=("Arial", 14))
    command_entry.pack(pady=10)

    # Adding a button to process typed commands
    submit_button = tk.Button(root, text="Submit", font=("Arial", 12), command=on_command_entry)
    submit_button.pack(pady=5)

    # Adding a button to listen for voice commands
    voice_button = tk.Button(root, text="Speak", font=("Arial", 12), command=on_voice_command)
    voice_button.pack(pady=5)

    # Start the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    print("WELCOME SIR! PLEASE SPEAK [WAKE UP] TO LOAD ME UP.")
    gui_interface()
