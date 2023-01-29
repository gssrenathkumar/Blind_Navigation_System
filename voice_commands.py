# Importing required packages
from subprocess import call

import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
import navigation_direction

# Initializing pyttsx3 voice command engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1)


def there_exists(terms):
    """Splitting the text into single parts"""
    for term in terms:
        if term in query:
            return True


def takeCommandMic():
    """Recognizer is used to initialize of listening from the microphone and store the data as text from
    the microphone input"""
    r = sr.Recognizer()
    print("Please Talk")
    # Initiaizing microphone as primary source to the program
    with sr.Microphone() as source:
        print("Listerning you....")
        # threshold is taken as 1 to remove 80 % of noise
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=2)

    try:
        # Printing the query
        print("Recognizing....")
        query = r.recognize_google(audio, language="en-IN")
        print(f"You: {query}")

    except Exception as e:
        print(e)
        return "none"
    return query


if __name__ == "__main__":

    while True:
        # Using NLP to split the query into multiple tokenize format
        query = takeCommandMic().lower()
        query1 = query
        query = word_tokenize(query)
        print(query)

        if there_exists(["where", "am", "i", "current", "location"]):
            navigation_direction.current_location_address()  # Getting location address
        elif there_exists(["what", "is", "in", "front", "of", "me"]):
            call(["python", "object_distance_detector.py"])  # Detecting live objects with sound alarm
        elif there_exists(["am", "im", "in", "correct", "path"]):
            navigation_direction.location_change_checks()
