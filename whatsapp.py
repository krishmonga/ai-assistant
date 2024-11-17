import pywhatkit
import pyttsx3
import datetime
import speech_recognition
import webbrowser
from bs4 import BeautifulSoup
from time import sleep
import os
from datetime import timedelta, datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=4)  # Added timeout for safety
            print("Understanding...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}\n")
        except speech_recognition.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return "None"
        except speech_recognition.UnknownValueError:
            print("Sorry, I couldn't understand that. Please repeat.")
            return "None"
        except speech_recognition.RequestError:
            print("Could not request results. Check your internet connection.")
            return "None"
    return query
def open_whatsapp_desktop():
    # Replace with the correct path where WhatsApp is installed on your system
    whatsapp_path = "https://web.whatsapp.com/"
    os.startfile(whatsapp_path)

def sendMessage():
    speak("Who do you want to message?")
    try:
        # Display options and handle user input
        recipient = int(input('''Choose a recipient:
1 - Person 1
2 - Person 2
Enter your choice: '''))

        # Handle different recipients
        if recipient == 1:
            phone_number = "+910000000000"  # Replace with actual number
        elif recipient == 2:
            phone_number = "+910000000001"  # Replace with actual number
        else:
            speak("Invalid option chosen.")
            return

        speak("What is the message?")
        message = input("Enter the message: ").strip()

        # Calculate the send time
        current_time = datetime.now()
        send_hour = current_time.hour
        send_minute = (current_time + timedelta(minutes=2)).minute

        # Send the message
        pywhatkit.sendwhatmsg(phone_number, message, send_hour, send_minute)
        speak("Message sent successfully.")
    except ValueError:
        speak("Invalid input. Please enter a valid choice.")
    except Exception as e:
        speak("An error occurred while sending the message.")
        print(f"Error: {e}")

if __name__ == "__main__":
    speak("Welcome! How can I assist you?")
    while True:
        command = takeCommand().lower()
        if "send a message" in command:
            sendMessage()
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
