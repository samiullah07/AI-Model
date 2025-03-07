import os
import eel
import sys
import traceback
import time
from backend.feature import *
from backend.command import *

def start():
    # Initialize eel with the frontend directory
    eel.init("frontend") 
    
    # Add error handling for Eel - only if not already exposed
    if 'handle_error' not in eel._exposed_functions:
        @eel.expose
        def handle_error(error):
            print(f"JavaScript error: {error}")
    
    # Play the assistant startup sound
    try:
        play_assistant_sound()
    except Exception as e:
        print(f"Error playing sound: {e}")
        traceback.print_exc()
    
    @eel.expose
    def init():
        try:
            eel.hideLoader()
            speak("Welcome to Jarvis")
            
            # Check if face recognition is available
            face_recognition_available = False
            try:
                import cv2
                face_recognition_available = True
            except ImportError:
                print("OpenCV not installed. Face recognition will be skipped.")
                face_recognition_available = False
            
            if face_recognition_available:
                try:
                    # Show face authentication UI
                    eel.showFaceAuth()
                    
                    # Import face recognition module
                    try:
                        from backend.face_recognition import verify_face_scan
                        
                        # Attempt face verification
                        if verify_face_scan():
                            # Face verification successful
                            eel.showFaceAuthSuccess()
                            time.sleep(2)  # Show success animation for 2 seconds
                            speak("Face scan successful. Welcome back!")
                        else:
                            # Face verification failed but we'll continue anyway
                            speak("Face verification skipped. Proceeding with normal startup.")
                    except ImportError as ie:
                        print(f"Error importing face recognition module: {ie}")
                        speak("Face authentication module not available. Proceeding with normal startup.")
                    except Exception as face_error:
                        print(f"Error during face authentication: {face_error}")
                        traceback.print_exc()
                        speak("Error during face authentication. Proceeding with normal startup.")
                except Exception as e:
                    print(f"Error in face authentication UI: {e}")
                    traceback.print_exc()
            
            # Continue with normal startup
            speak("Welcome to Your Assistant")
            eel.hideStart()
            try:
                play_assistant_sound()
            except Exception as sound_error:
                print(f"Error playing assistant sound: {sound_error}")
                
        except Exception as e:
            print(f"Error in init: {e}")
            traceback.print_exc()
            # Try to recover
            try:
                eel.hideStart()
            except Exception as recovery_error:
                print(f"Error during recovery: {recovery_error}")
    
    # Start the browser with the Jarvis UI
    try:
        os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
    except Exception as e:
        print(f"Error starting Edge browser: {e}")
        # Try an alternative browser if Edge fails
        try:
            os.system('start chrome.exe --app="http://127.0.0.1:8000/index.html"')
        except Exception as e2:
            print(f"Error starting Chrome browser: {e2}")
            try:
                # Try a generic browser open
                os.system('start http://127.0.0.1:8000/index.html')
            except:
                print("Could not start browser. Please open http://127.0.0.1:8000/index.html manually.")
    
    # Start the Eel web server with better error handling
    try:
        eel.start("index.html", mode=None, host="localhost", block=True)
    except Exception as e:
        print(f"Error starting Eel: {e}")
        traceback.print_exc()
        sys.exit(1)

