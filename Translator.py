import googletrans
from googletrans import Translator  # pip install googletrans==4.0.0-rc1
from gtts import gTTS  # pip install gtts
import pyttsx3
import speech_recognition as sr
import os
from playsound import playsound  # pip install playsound==1.2.2

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=4)
            print("Understanding...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}\n")
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            speak("No speech detected. Please try again.")
            return "None"
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please repeat.")
            speak("Sorry, I couldn't understand. Please repeat.")
            return "None"
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")
            speak("Could not connect to the internet. Please check your connection.")
            return "None"
    return query

def translategl(query):
    speak("Sure, let me handle that.")
    print("Available languages:")
    for lang_code, lang_name in list(googletrans.LANGUAGES.items())[:10]:  # Show a subset of languages
        print(f"{lang_code}: {lang_name}")
    print("For the full list, refer to the documentation.")
    
    translator = Translator()

    speak("Enter the language code for translation from the displayed list.")
    b = input("To_Lang (Enter language code, e.g., 'hi' for Hindi): ").strip()

    if b not in googletrans.LANGUAGES:
        print("Invalid language code. Please try again.")
        speak("The language code you entered is invalid.")
        return

    try:
        # Translate text
        text_to_translate = translator.translate(query, src="auto", dest=b)
        translated_text = text_to_translate.text
        print(f"Translated Text: {translated_text}")

        # Convert to audio using gTTS
        speakgl = gTTS(text=translated_text, lang=b, slow=False)
        temp_audio_file = "voice.mp3"
        speakgl.save(temp_audio_file)

        # Play the translated audio
        playsound(temp_audio_file)

        # Clean up temporary file
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
    except Exception as e:
        print("Unable to translate or play the translated text.")
        print(f"Error: {e}")
        speak("Sorry, I could not complete the translation.")

# Main execution
if __name__ == "__main__":
    while True:
        speak("Please say something to translate.")
        query = takeCommand()
        if query and query != "None":
            translategl(query)
        else:
            speak("Would you like to try again? Say yes or no.")
            retry = takeCommand()
            if retry.lower() in ["no", "exit", "quit"]:
                speak("Goodbye!")
                break
