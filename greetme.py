import pyttsx3
import datetime

# Initialize the pyttsx3 engine
try:
    engine = pyttsx3.init()
except Exception as e:
    print("Error initializing the speech engine:", e)
    engine = None

# Function to configure the voice
def set_voice(voice_type="male"):
    """Set the assistant's voice to male or female."""
    if engine:
        voices = engine.getProperty("voices")
        if voice_type == "female" and len(voices) > 1:
            engine.setProperty("voice", voices[1].id)  # Female voice
        else:
            engine.setProperty("voice", voices[0].id)  # Default to male voice
    else:
        print("Voice engine not available.")

# Function to set speaking rate
def set_rate(rate=170):
    """Set the speech rate of the assistant."""
    if engine:
        engine.setProperty("rate", rate)

# Function to speak the provided audio
def speak(audio):
    """Speak the provided text and print it for visual feedback."""
    print(f"Assistant: {audio}")
    if engine:
        engine.say(audio)
        engine.runAndWait()

# Function to determine and provide a greeting
def greetme():
    """Greet the user based on the current time and date."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    
    # Add special occasion greetings
    special_dates = {
        "01-01": "Happy New Year!",
        "12-25": "Merry Christmas!",
        "07-04": "Happy Independence Day!"  # Example of adding another date
    }
    current_date = datetime.datetime.now().strftime("%m-%d")
    if current_date in special_dates:
        greeting = special_dates[current_date]
    
    speak(greeting)
    speak("I am your virtual assistant. How can I help you?")

if __name__ == "__main__":
    if engine:
        # Configure voice and rate
        set_voice("male")  # Change to "female" for a female voice
        set_rate(170)      # Adjust the rate as needed
        
        # Greet the user
        greetme()
    else:
        print("The speech engine could not be initialized. Please check your system.")
