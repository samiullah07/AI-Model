import datetime
import os
import random
import re
import time
import eel
import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')
print(f"Available voices: {len(voices)}")

# Try to find a good voice
voice_found = False
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        print(f"Using female voice: {voice.name}")
        voice_found = True
        break

# If no female voice, use the default voice
if not voice_found and len(voices) > 0:
    engine.setProperty('voice', voices[0].id)
    print(f"Using default voice: {voices[0].name}")

# Set properties
engine.setProperty('rate', 150)  # Speed of speech

def speak(text):
    """Speak the given text and display it on the UI."""
    print(f"Response: {text}")
    try:
        # Display the message on the UI
        eel.DisplayMessage(text)
        # Speak the text
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")
        # Try to speak even if display fails
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as speak_error:
            print(f"Error speaking: {speak_error}")

def takecommand():
    """Listen for voice input and return the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        return query
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return ""

@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            eel.ShowHood()
            return  # Exit if no query is received
        print(query)
        eel.senderText(query)
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)
    
    try:
        if query:
            # Check for music-related queries first
            if any(word in query.lower() for word in ["play", "song", "music", "listen"]):
                from backend.feature import PlayYoutube
                PlayYoutube(query)
            # Check for specific artist songs
            elif "songs" in query.lower():
                from backend.feature import PlayYoutube
                PlayYoutube(query)  # Pass the query directly to PlayYoutube
            # Check for search queries
            elif any(word in query.lower() for word in ["search for", "look up", "find information"]):
                search_term = query.lower().replace("search for", "").replace("look up", "").replace("find information", "").strip()
                if search_term:
                    speak(f"Searching for {search_term}")
                    import webbrowser
                    webbrowser.open(f"https://www.google.com/search?q={search_term}")
                else:
                    speak("What would you like to search for?")
            # Check for open commands
            elif "open" in query:
                from backend.feature import openCommand
                openCommand(query)
            # Check for WhatsApp commands
            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        message_text = takecommand()  # Ask for the message text
                        if not message_text:
                            message_text = "Hello"
                            speak("Using default message: Hello")
                    elif "call" in query:
                        flag = 'call'
                        message_text = ""
                    else:
                        flag = 'video call'
                        message_text = ""
                    whatsApp(Phone, message_text, flag, name)
            # Check for YouTube queries
            elif "on youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
            # For all other queries, use the chatbot
            else:
                from backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
    
    eel.ShowHood()

