import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Adjust speech speed
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Set voice

def speak(audio):
    """Speaks the provided audio string."""
    engine.say(audio)
    engine.runAndWait()

def take_command():
    """Listens for a command from the user."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=6)
        except sr.WaitTimeoutError:
            print("No response detected. Please try again.")
            return "None"
        except Exception as e:
            print("Error capturing audio:", e)
            return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return "None"
    except sr.RequestError:
        print("Internet connection error.")
        return "None"
    return query.lower()

def search_google(query):
    """Searches Google for the given query."""
    query = query.replace("google", "").replace("search", "").strip()
    speak(f"Searching Google for {query}.")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    try:
        result = wikipedia.summary(query, sentences=1)
        print(result)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("The query is too broad. Please try to be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No results found on Wikipedia for this query.")
    except Exception as e:
        print("Error searching Google:", e)
        speak("I couldn't find a relevant result.")

def search_youtube(query):
    """Searches YouTube for the given query."""
    query = query.replace("youtube", "").replace("search", "").strip()
    speak(f"Searching YouTube for {query}.")
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)

def search_wikipedia(query):
    """Searches Wikipedia for the given query."""
    query = query.replace("wikipedia", "").replace("search", "").strip()
    speak(f"Searching Wikipedia for {query}.")
    try:
        result = wikipedia.summary(query, sentences=2)
        print(result)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("The query is too broad. Please try to be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No Wikipedia page found for this query.")
    except Exception as e:
        print("Error searching Wikipedia:", e)
        speak("Sorry, I could not find relevant information.")

# Main execution loop
if __name__ == "__main__":
    speak("Hello, I am your virtual assistant. How can I help you?")
    while True:
        query = take_command()
        if query == "none":
            continue

        if "google" in query:
            search_google(query)
        elif "youtube" in query:
            search_youtube(query)
        elif "wikipedia" in query:
            search_wikipedia(query)
        elif "exit" in query or "stop" in query:
            speak("Goodbye! Have a great day!")
            break
