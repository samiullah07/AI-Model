import os
import time
import traceback
from backend.command import speak

def init_face_recognition():
    """Initialize face recognition components."""
    try:
        import cv2
        print("OpenCV is available. Face recognition can be used.")
        return True
    except ImportError:
        print("OpenCV is not installed. Face recognition will not be available.")
        return False

def verify_face_scan():
    """
    Simplified face scan verification.
    In a real implementation, this would use OpenCV to detect and recognize faces.
    """
    try:
        import cv2
        
        # Check if camera is available
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            speak("Camera not available. Skipping face scan.")
            return False
        
        # Simulate face scanning
        speak("Scanning face. Please look at the camera.")
        print("Scanning face...")
        
        # Show camera feed for a few seconds
        start_time = time.time()
        face_detected = False
        
        # Load face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        while time.time() - start_time < 5:  # Scan for 5 seconds
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Draw rectangle around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                face_detected = True
            
            # Display the frame
            cv2.imshow('Face Scanning', frame)
            
            # Break on ESC key
            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        
        if face_detected:
            speak("Face scan successful!")
            return True
        else:
            speak("No face detected. Proceeding with normal startup.")
            return False
            
    except Exception as e:
        print(f"Error in face scanning: {e}")
        traceback.print_exc()
        speak("Error during face scanning. Proceeding with normal startup.")
        return False

