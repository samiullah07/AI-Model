import os
import re
import struct
import subprocess
import time
import webbrowser
import eel
import random
import datetime
import pygame
from backend.command import speak
from backend.config import ASSISTANT_NAME
import sqlite3
from shlex import quote
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import requests
import json

# Initialize database connection
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# Initialize pygame mixer
pygame.mixer.init()

# Define the function to play sound
@eel.expose
def play_assistant_sound():
    # Use relative path for better portability
    sound_file = os.path.join("frontend", "assets", "audio", "start_sound.mp3")
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing sound: {e}")
        # Try alternative sound file if the first one fails
        try:
            alt_sound_file = os.path.join("frontend", "assets", "audio", "jarvis_voice.mp3")
            pygame.mixer.music.load(alt_sound_file)
            pygame.mixer.music.play()
        except Exception as e2:
            print(f"Error playing alternative sound: {e2}")

def extract_yt_term(query):
    """Extract search term from a YouTube query."""
    # Check for "play X on YouTube" pattern
    match = re.search(r'play\s+(.*?)\s+on\s+youtube', query.lower())
    if match:
        return match.group(1)
    
    # Check for "play X" pattern
    match = re.search(r'play\s+(.*)', query.lower())
    if match:
        return match.group(1)
    
    return None

def remove_words(text, words_to_remove):
    """Remove specific words from a text string."""
    result = text.lower()
    for word in words_to_remove:
        result = result.replace(word.lower(), "")
    
    # Clean up extra spaces
    result = re.sub(r'\s+', ' ', result).strip()
    return result

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()
    
    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])
            elif len(results) == 0: 
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except:
                        speak("not found")
        except Exception as e:
            speak(f"Something went wrong: {str(e)}")

def PlayYoutube(query):
    # Check if this is an artist + "songs" query
    if "songs" in query.lower():
        artist = query.lower().replace("songs", "").strip()
        if artist:
            search_term = f"{artist} songs"
            speak(f"Playing songs by {artist} on YouTube")
            kit.playonyt(search_term)
            return
    
    # First check if there's a specific term to extract
    search_term = extract_yt_term(query)
    
    # If no specific term, check if it's a general music request
    if not search_term and any(word in query.lower() for word in ["song", "music", "play"]):
        # Extract potential artist or song name
        words_to_remove = [ASSISTANT_NAME, "play", "on", "youtube", "song", "music", "some"]
        potential_term = remove_words(query, words_to_remove).strip()
        
        if potential_term:
            search_term = potential_term
        else:
            # If no specific term found, play some popular music
            popular_music = [
                "top hits playlist",
                "popular songs 2023",
                "best music this week",
                "trending songs",
                "music mix"
            ]
            search_term = random.choice(popular_music)
            speak(f"I'll play some {search_term} for you")
    
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("I couldn't understand what to play on YouTube")

def hotword():
    """
    This function implements a simplified hotword detection.
    Since the Picovoice Porcupine requires an access key, we're using
    a simplified approach that doesn't require an access key.
    """
    print("Starting hotword detection (simplified mode)")
    
    try:
        # Simple polling approach - check every 2 seconds
        while True:
            time.sleep(2)
            # This is a placeholder - in a real implementation, you'd check for a hotword
            # using a different library or method
    except KeyboardInterrupt:
        print("Hotword detection stopped by user")
    except Exception as e:
        print(f"Error in hotword detection: {e}")

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
                      ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        
        if results and len(results) > 0:
            mobile_number_str = str(results[0][0])

            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str

            return mobile_number_str, query
        else:
            speak('Contact not found')
            return 0, 0
    except Exception as e:
        speak(f'Error finding contact: {str(e)}')
        return 0, 0

def whatsApp(Phone, message, flag, name):
    if Phone == 0:
        return
        
    if flag == 'message':
        target_tab = 12
        jarvis_message = "Message sent successfully to " + name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "Calling " + name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "Starting video call with " + name

    # Encode the message for URL
    encoded_message = quote(message)
    
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    try:
        # Open WhatsApp with the constructed URL using cmd.exe
        subprocess.run(full_command, shell=True)
        time.sleep(5)
        subprocess.run(full_command, shell=True)
        
        pyautogui.hotkey('ctrl', 'f')

        for i in range(1, target_tab):
            pyautogui.hotkey('tab')

        pyautogui.hotkey('enter')
        speak(jarvis_message)
    except Exception as e:
        speak(f"Error with WhatsApp: {str(e)}")

def chatBot(query):
    """
    Enhanced chatbot function that uses a comprehensive local response system.
    """
    try:
        # Check if this is a music/song request for a specific artist
        if "songs" in query.lower():
            # Extract the artist name
            artist = query.lower().replace("songs", "").strip()
            if artist:
                speak(f"Playing songs by {artist}")
                PlayYoutube(f"{artist} songs")
                return f"Playing songs by {artist}"
        
        # Generate a response using our enhanced local system
        response = generate_response(query)
        print(f"Response: {response}")
        speak(response)
        return response
    except Exception as e:
        error_msg = f"Error with chatbot: {str(e)}"
        print(error_msg)
        speak("Sorry, I encountered an error. Please try again.")
        return error_msg

# Knowledge base for common topics
knowledge_base = {
    "atif aslam": [
        "Atif Aslam is a famous Pakistani playback singer, songwriter, and actor. He's known for his powerful vocals and has sung many hit songs in Bollywood and Pakistani music industry.",
        "Atif Aslam is one of the most popular singers in South Asia. Some of his famous songs include 'Tera Hone Laga Hoon', 'Pehli Nazar Mein', and 'Jeena Jeena'.",
        "Atif Aslam started his career with the band 'Jal' and later became a successful solo artist. He has a huge fan following across Pakistan, India, and many other countries."
    ],
    "arijit singh": [
        "Arijit Singh is a popular Indian playback singer known for his soulful voice. He has sung numerous hit songs in Bollywood films.",
        "Arijit Singh rose to fame with the song 'Tum Hi Ho' from the movie Aashiqui 2. Some of his other popular songs include 'Channa Mereya', 'Ae Dil Hai Mushkil', and 'Gerua'.",
        "Arijit Singh is one of the most successful and versatile singers in the Indian music industry, known for his emotional and melodious singing style."
    ],
    "salman khan": [
        "Salman Khan is a popular Indian actor, film producer, and television personality. He is one of the most commercially successful actors in Bollywood.",
        "Salman Khan is known for his roles in films like 'Dabangg', 'Tiger Zinda Hai', 'Bajrangi Bhaijaan', and 'Sultan'. He has a massive fan following in India and around the world.",
        "Salman Khan also hosts the popular reality TV show 'Bigg Boss' and is known for his charitable work through his foundation 'Being Human'."
    ],
    "shahrukh khan": [
        "Shah Rukh Khan, often called SRK or King Khan, is one of the most successful actors in Indian cinema. He's known as the 'King of Bollywood'.",
        "Shah Rukh Khan has starred in numerous blockbuster films including 'Dilwale Dulhania Le Jayenge', 'Kuch Kuch Hota Hai', 'Chennai Express', and 'Pathaan'.",
        "Shah Rukh Khan is known for his charm, wit, and versatility as an actor. He has a global fan following and has received numerous awards for his performances."
    ],
    "tilawat": [
        "Tilawat refers to the recitation of the Quran, the holy book of Islam. It involves reading the Quran with proper pronunciation and intonation.",
        "Tilawat is an important practice in Islam, and there are specific rules and techniques for reciting the Quran correctly, known as Tajweed.",
        "Would you like me to search for Tilawat recitations online? Just say 'play Tilawat' and I can find some for you."
    ],
    "action movies": [
        "Action movies are a popular film genre characterized by exciting sequences, physical stunts, chases, fights, and heroic main characters.",
        "Some popular action movies include 'Die Hard', 'The Matrix', 'Mad Max: Fury Road', 'John Wick', and the 'Mission: Impossible' series.",
        "Would you like me to recommend some action movies or play a trailer for you? Just say 'play action movie trailer'."
    ],
    "google": [
        "Google is a multinational technology company that specializes in Internet-related services and products, including search engines, online advertising, cloud computing, and software.",
        "Google was founded in 1998 by Larry Page and Sergey Brin while they were Ph.D. students at Stanford University. It's now one of the world's most valuable companies.",
        "Google's search engine is the most widely used web-based search engine, handling more than 3.5 billion searches per day."
    ],
    "youtube": [
        "YouTube is a video-sharing platform where users can upload, view, rate, share, and comment on videos. It was created in 2005 and is now owned by Google.",
        "YouTube is one of the most visited websites globally, with over 2 billion logged-in monthly users who watch over a billion hours of video daily.",
        "YouTube allows creators to earn money through the YouTube Partner Program, which shares advertising revenue with content creators."
    ],
    "weather": [
        "I don't have access to real-time weather data, but you can check the current weather by looking outside or using a weather app on your device.",
        "Weather refers to the state of the atmosphere at a specific place and time, including factors like temperature, humidity, precipitation, and wind.",
        "If you'd like to know the weather forecast, I recommend checking a weather service like Weather.com or your local news website."
    ],
    "time": [
        f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}.",
        f"It's currently {datetime.datetime.now().strftime('%I:%M %p')} on {datetime.datetime.now().strftime('%A, %B %d, %Y')}.",
        f"The time right now is {datetime.datetime.now().strftime('%I:%M %p')}."
    ],
    "date": [
        f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}.",
        f"The current date is {datetime.datetime.now().strftime('%B %d, %Y')}.",
        f"It's {datetime.datetime.now().strftime('%A, %B %d, %Y')} today."
    ],
    "jarvis": [
        f"I am {ASSISTANT_NAME}, your personal AI assistant. I'm here to help you with various tasks and answer your questions.",
        f"My name is {ASSISTANT_NAME}. I'm a voice-activated assistant designed to help you with information, tasks, and entertainment.",
        f"I'm {ASSISTANT_NAME}, an AI assistant created to make your life easier. I can help with information, play music, open applications, and more."
    ],
    "music": [
        "I can play music for you on YouTube. Just say 'play' followed by the song or artist name.",
        "What kind of music do you enjoy? I can play songs for you if you tell me what you'd like to hear.",
        "I can help you listen to music. Try saying 'play some rock music' or 'play songs by [artist name]'."
    ],
    "joke": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call a fake noodle? An impasta!",
        "Why couldn't the bicycle stand up by itself? It was two tired!",
        "How does a penguin build its house? Igloos it together!",
        "Why did the math book look sad? Because it had too many problems.",
        "What's orange and sounds like a parrot? A carrot!",
        "Why did the chicken join a band? Because it had the drumsticks!",
        "What do you call a fish wearing a crown? King of the sea!",
        "How do you organize a space party? You planet!"
    ],
    "fact": [
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
        "A group of flamingos is called a 'flamboyance'.",
        "The average person will spend six months of their life waiting for red lights to turn green.",
        "The world's oldest known living tree is over 5,000 years old.",
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat.",
        "A day on Venus is longer than a year on Venus. It takes 243 Earth days to rotate once on its axis, but only 225 Earth days to go around the Sun.",
        "Octopuses have three hearts, nine brains, and blue blood.",
        "The Great Wall of China is not visible from space with the naked eye, contrary to popular belief.",
        "Bananas are berries, but strawberries are not.",
        "A bolt of lightning is five times hotter than the surface of the sun."
    ]
}

def generate_response(user_input):
    """Generate a response based on the user input using pattern matching and knowledge base."""
    user_input = user_input.lower()
    
    # Check for music/song requests with artist names
    if "songs" in user_input:
        # Extract the artist name
        artist = user_input.replace("songs", "").strip()
        if artist:
            return f"I can play songs by {artist} for you. Just say 'play {artist} songs'."
    
    # Check if the query matches any entry in our knowledge base
    for topic, responses in knowledge_base.items():
        if topic in user_input:
            return random.choice(responses)
    
    # Check for specific words or phrases in the query
    
    # Music-related queries
    if any(word in user_input for word in ["song", "songs", "music", "playlist", "sing", "artist", "album"]):
        music_responses = [
            "I can help you with music! Would you like me to play a song on YouTube?",
            "I love music too! You can ask me to play specific songs on YouTube by saying 'play [song name] on YouTube'.",
            "Music is great! Tell me what artist or song you'd like to hear, and I can play it for you on YouTube.",
            "I can play music for you. Just say 'play [song name]' and I'll search for it on YouTube.",
            "What kind of music do you enjoy? You can ask me to play specific genres or artists."
        ]
        return random.choice(music_responses)
    
    # Movie-related queries
    elif any(word in user_input for word in ["movie", "movies", "film", "cinema", "actor", "actress"]):
        movie_responses = [
            "I can tell you about various movies and actors. What specific movie or actor are you interested in?",
            "Movies are great! Are you looking for information about a specific film or actor?",
            "I know about many popular movies and actors. What would you like to know?",
            "Are you interested in Bollywood or Hollywood movies? I can provide information about both."
        ]
        return random.choice(movie_responses)
    
    # Search engine queries
    elif any(word in user_input for word in ["search", "find", "look up", "search for"]):
        search_responses = [
            "I can help you search the web. What would you like to search for?",
            "Would you like me to open Google for you? Just say 'open google'.",
            "I can search for information online. Try saying 'search for [your query]'.",
            "Need to find something online? I can help you search for it."
        ]
        return random.choice(search_responses)
    
    # System-related queries
    elif any(phrase in user_input for phrase in ["system", "computer", "pc", "laptop", "windows", "mac", "device"]):
        system_responses = [
            "I can help with some basic system tasks. Would you like to open a specific application?",
            "Need help with your computer? I can open applications or provide basic information.",
            "I can assist with some system operations. What would you like to do?",
            "Your computer is running well. Is there a specific program you'd like to open?"
        ]
        return random.choice(system_responses)
    
    # Greetings
    elif any(word in user_input for word in ["hello", "hi", "hey", "greetings"]):
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to assist you.",
            "Greetings! How may I be of service?"
        ]
        return random.choice(greetings)
    
    # Well-being inquiries
    elif any(phrase in user_input for phrase in ["how are you", "how're you", "how you doing", "how's it going"]):
        responses = [
            "I'm functioning well, thank you for asking!",
            "All systems operational and ready to assist you.",
            "I'm doing great! How about you?",
            "I'm at your service and ready to help."
        ]
        return random.choice(responses)
    
    # Gratitude
    elif any(word in user_input for word in ["thanks", "thank you", "appreciate"]):
        responses = [
            "You're welcome! Is there anything else I can help with?",
            "Happy to help! Let me know if you need anything else.",
            "My pleasure! What else can I do for you?",
            "Anytime! I'm here whenever you need assistance."
        ]
        return random.choice(responses)
    
    # Farewells
    elif any(word in user_input for word in ["bye", "goodbye", "see you", "farewell"]):
        farewells = [
            "Goodbye! Have a great day!",
            "See you later! I'll be here when you need me.",
            "Farewell! Call on me anytime you need assistance.",
            "Until next time! Stay well."
        ]
        return random.choice(farewells)
    
    # Identity questions
    elif any(phrase in user_input for phrase in ["who are you", "what are you", "your name"]):
        return f"I'm {ASSISTANT_NAME}, your personal AI assistant. I'm here to help you with various tasks and answer your questions."
    
    # Capabilities
    elif any(phrase in user_input for phrase in ["what can you do", "your abilities", "help me with", "your features"]):
        return "I can help you with various tasks like opening applications, searching the web, playing videos on YouTube, answering questions, telling jokes, and providing information. Just ask me what you need!"
    
    # Hearing check
    elif "hear me" in user_input:
        return "Yes, I can hear you clearly. How can I help you today?"
    
    # Name questions
    elif "my name" in user_input:
        return "I don't have that information stored. Would you like to tell me your name?"
    
    # Try to extract a name or entity from the query
    words = user_input.split()
    if len(words) == 1 and len(words[0]) > 2:  # Single word query that's not too short
        entity = words[0].capitalize()
        return f"I don't have specific information about {entity}. Would you like me to search for it online? Just say 'search for {entity}'."
    
    # Default responses for unknown queries
    default_responses = [
        "I'm not sure how to respond to that. Could you try asking something else?",
        "I don't have information on that topic yet. Is there something else I can help with?",
        "I'm still learning and don't know how to answer that question. Could you try a different query?",
        "That's beyond my current capabilities. Is there another way I can assist you?",
        "I'm afraid I don't understand that request. Could you rephrase or ask me something different?"
    ]
    return random.choice(default_responses)

