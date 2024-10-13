import speech_recognition
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

# Initialize the speech recognition and text-to-speech engine
engine = pyttsx3.init()

def takecommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=4)
        except Exception as e:
            print("Sorry, I couldn't hear that. Please repeat.")
            return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def searchGoogle(query):
    if "google" in query:
        query = query.replace("google", "").replace("jarvis", "").replace("google search", "")
        speak("This is what I found on Google.")
        try:
            pywhatkit.search(query)
            result = wikipedia.summary(query, sentences=1)
            print(result)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("The query is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("No Wikipedia page found for this query.")
        except:
            speak("No speakable output available.")

def searchyoutube(query):
    if "youtube" in query:
        query = query.replace("youtube", "").replace("jarvis", "").replace("search", "")
        speak("Searching on YouTube.")
        web = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Here are the results from YouTube.")

def searchwikipedia(query):
    if "wikipedia" in query:
        query = query.replace("wikipedia", "").replace("jarvis", "").replace("search", "")
        speak("Searching on Wikipedia.")
        try:
            result = wikipedia.summary(query, sentences=1)
            print(result)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("The query is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("No Wikipedia page found for this query.")
        except:
            speak("Unable to retrieve information.")

if __name__ == "__main__":
    speak("Hello, I am your virtual assistant. How can I help you?")
    while True:
        query = takecommand()

        if "google" in query:
            searchGoogle(query)
        elif "youtube" in query:
            searchyoutube(query)
        elif "wikipedia" in query:
            searchwikipedia(query)
