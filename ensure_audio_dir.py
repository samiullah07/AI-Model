import os

def ensure_audio_directory():
    """Ensure the audio directory exists and create placeholder files if needed."""
    audio_dir = "frontend/assets/audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    # Create placeholder files if they don't exist
    start_sound = os.path.join(audio_dir, "start_sound.mp3")
    jarvis_voice = os.path.join(audio_dir, "jarvis_voice.mp3")
    
    if not os.path.exists(start_sound):
        print(f"Creating placeholder file: {start_sound}")
        with open(start_sound, 'wb') as f:
            f.write(b'')
    
    if not os.path.exists(jarvis_voice):
        print(f"Creating placeholder file: {jarvis_voice}")
        with open(jarvis_voice, 'wb') as f:
            f.write(b'')
    
    print("Audio directory and placeholder files created successfully.")

if __name__ == "__main__":
    ensure_audio_directory()

