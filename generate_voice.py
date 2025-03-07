import os
import pyttsx3

def generate_voice_file(text, output_file):
    """Generate a voice file using pyttsx3."""
    engine = pyttsx3.init()
    
    # Get available voices
    voices = engine.getProperty('voices')
    print(f"Found {len(voices)} voices")
    
    # Try to find a good voice
    voice_found = False
    
    # First try to find a female voice
    for voice in voices:
        if "female" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            print(f"Using female voice: {voice.name}")
            voice_found = True
            break
    
    # If no female voice, try to find a male voice that's not the default
    if not voice_found:
        for voice in voices:
            if "male" in voice.name.lower() and voice.id != voices[0].id:
                engine.setProperty('voice', voice.id)
                print(f"Using male voice: {voice.name}")
                voice_found = True
                break
    
    # Fall back to the first voice if no suitable voice found
    if not voice_found and len(voices) > 0:
        engine.setProperty('voice', voices[0].id)
        print(f"Using default voice: {voices[0].name}")
    
    # Set properties
    engine.setProperty('rate', 150)  # Speed of speech
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save to file
    print(f"Generating voice file: {output_file}")
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    
    if os.path.exists(output_file):
        print(f"Voice file generated successfully: {output_file}")
    else:
        print(f"Failed to generate voice file: {output_file}")

if __name__ == "__main__":
    # Create the directory structure if it doesn't exist
    audio_dir = "frontend/assets/audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    # Generate the Jarvis voice files
    generate_voice_file(
        "I am Jarvis, your personal assistant. How can I help you today?",
        os.path.join(audio_dir, "jarvis_voice.mp3")
    )
    
    generate_voice_file(
        "Jarvis initialized and ready for commands.",
        os.path.join(audio_dir, "start_sound.mp3")
    )
    
    print("Voice generation complete.")

