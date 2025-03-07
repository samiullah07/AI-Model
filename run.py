import multiprocessing
import time
import sys
import os
import traceback

def load_env_vars():
    """Load environment variables from .env file if it exists."""
    try:
        from dotenv import load_dotenv
        env_file = ".env"
        if os.path.exists(env_file):
            print("Loading environment variables from .env file...")
            load_dotenv(override=True)
            print("Environment variables loaded.")
        else:
            print("No .env file found. Using system environment variables.")
    except ImportError:
        print("python-dotenv not installed. Using system environment variables.")
        # Try to load manually if dotenv is not available
        env_file = ".env"
        if os.path.exists(env_file):
            print("Loading environment variables manually...")
            with open(env_file, "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value
            print("Environment variables loaded.")

def startJarvis():
    print("Process 1 Starting...")
    try:
        # Create and apply the Eel patch directly here instead of importing it
        import eel
        
        # Store the original _process_message function
        original_process_message = eel._process_message

        # Define our patched version that handles missing 'value' key
        def patched_process_message(message, websocket):
            try:
                # Check if this is an error response without a 'value' key
                if 'return' in message and 'status' in message and message.get('status') == 'error':
                    # Handle error responses properly
                    call_id = message.get('return')
                    if call_id in eel._call_return_values:
                        # Set a default error value
                        eel._call_return_values[call_id] = None
                        print(f"Handled error response for call ID {call_id}")
                    return
                
                # Otherwise, use the original function
                return original_process_message(message, websocket)
            except Exception as e:
                print(f"Error in patched _process_message: {e}")
                traceback.print_exc()

        # Apply the patch
        eel._process_message = patched_process_message

        # Add a global error handler with a different name to avoid conflicts
        @eel.expose
        def patch_handle_error(error_message):
            print(f"JavaScript error reported by patch: {error_message}")
            
        # Now import and start the main application
        from main import start
        start()
    except Exception as e:
        print(f"Error in Jarvis process: {e}")
        traceback.print_exc()

def listenHotword():
    print("Process 2 Starting...")
    try:
        from backend.feature import hotword
        hotword()
    except Exception as e:
        print(f"Error in hotword process: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment variables from .env file if it exists
    load_env_vars()
    
    # First, make sure the audio files exist
    audio_dir = "frontend/assets/audio"
    start_sound = os.path.join(audio_dir, "start_sound.mp3")
    jarvis_voice = os.path.join(audio_dir, "jarvis_voice.mp3")
    
    if not os.path.exists(start_sound) or not os.path.exists(jarvis_voice):
        print("Voice files not found. Generating them now...")
        try:
            import generate_voice
            # This will create the voice files
        except Exception as e:
            print(f"Error generating voice files: {e}")
            traceback.print_exc()
            # Create the directory if it doesn't exist
            os.makedirs(audio_dir, exist_ok=True)
            # Create empty files as placeholders
            with open(start_sound, 'wb') as f:
                f.write(b'')
            with open(jarvis_voice, 'wb') as f:
                f.write(b'')
    
    # Create processes
    process1 = multiprocessing.Process(target=startJarvis)
    process2 = multiprocessing.Process(target=listenHotword)
    
    try:
        # Start processes
        process1.start()
        process2.start()
        
        # Wait for the main process to complete
        process1.join()
        
        # Terminate the hotword process if it's still running
        if process2.is_alive():
            print("Terminating hotword detection process...")
            process2.terminate()
            process2.join(timeout=5)
            
            # Force kill if it doesn't terminate gracefully
            if process2.is_alive():
                print("Force killing hotword process...")
                if sys.platform == 'win32':
                    os.system(f'taskkill /F /PID {process2.pid}')
                else:
                    os.system(f'kill -9 {process2.pid}')
    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Shutting down...")
        if process1.is_alive():
            process1.terminate()
        if process2.is_alive():
            process2.terminate()
    
    except Exception as e:
        print(f"Error in main process: {e}")
        traceback.print_exc()
    
    finally:
        # Make sure all processes are terminated
        if process1.is_alive():
            process1.terminate()
            process1.join(timeout=2)
        
        if process2.is_alive():
            process2.terminate()
            process2.join(timeout=2)
        
        print("System is terminated.")

