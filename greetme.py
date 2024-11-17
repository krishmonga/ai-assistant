import pyttsx3
import datetime

# Initialize the pyttsx3 engine
try:
    engine = pyttsx3.init()
except Exception as e:
    print("Error initializing the speech engine:", e)

# Function to configure the voice
def set_voice(voice_type="male"):
    voices = engine.getProperty("voices")
    if voice_type == "female":
        engine.setProperty("voice", voices[1].id)  # Female voice
    else:
        engine.setProperty("voice", voices[0].id)  # Male voice

# Function to set speaking rate
def set_rate(rate=170):
    engine.setProperty("rate", rate)

# Function to speak the provided audio
def speak(audio):
    print(f"Assistant: {audio}")  # Print the message for visual feedback
    engine.say(audio)
    engine.runAndWait()

# Function to greet the user based on the time of day
def greetme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    
    # Add special greetings for certain occasions
    current_date = datetime.datetime.now().strftime("%m-%d")
    if current_date == "01-01":
        greeting = "Happy New Year!"
    elif current_date == "12-25":
        greeting = "Merry Christmas!"
    
    speak(greeting)
    speak("I am your virtual assistant. How can I help you?")

if __name__ == "__main__":
    # Configure voice and rate
    set_voice("male")  # Change to "female" for a female voice
    set_rate(170)      # Adjust the rate as needed
    
    # Greet the user
    greetme()
