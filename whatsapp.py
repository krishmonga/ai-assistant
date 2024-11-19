import pywhatkit
import pyttsx3
import speech_recognition
import os
from datetime import datetime, timedelta

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    """Speak the given audio string."""
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Take voice input from the user."""
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.energy_threshold = 300
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Understanding...")
            query = recognizer.recognize_google(audio, language='en-in')
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
    return query.lower()

def sendMessage():
    """Send a WhatsApp message using pywhatkit."""
    contacts = {
        "person 1": "+910000000000",  # Replace with actual numbers
        "person 2": "+910000000001",
    }

    speak("Who do you want to message?")
    recipient = takeCommand()
    if recipient in contacts:
        phone_number = contacts[recipient]
    else:
        speak("Recipient not found in contact list.")
        return

    speak("What is the message?")
    message = takeCommand()
    if message == "None":
        speak("No message detected. Please try again.")
        return

    # Calculate send time
    current_time = datetime.now()
    send_hour = current_time.hour
    send_minute = current_time.minute + 2
    if send_minute >= 60:
        send_hour = (send_hour + 1) % 24
        send_minute = send_minute - 60

    try:
        # Send the message
        pywhatkit.sendwhatmsg(phone_number, message, send_hour, send_minute)
        speak(f"Message to {recipient} has been scheduled.")
    except Exception as e:
        speak("An error occurred while sending the message.")
        print(f"Error: {e}")

if __name__ == "__main__":
    speak("Welcome! How can I assist you?")
    while True:
        command = takeCommand()
        if "send a message" in command:
            sendMessage()
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        elif command != "None":
            speak("I didn't understand that. Please try again.")
