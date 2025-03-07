import os
import sys
import subprocess

def setup_face_recognition():
    """
    Set up face recognition dependencies.
    """
    print("\n=== Face Recognition Setup ===\n")
    
    # Check if OpenCV is installed
    try:
        import cv2
        print("✓ OpenCV is already installed.")
    except ImportError:
        print("Installing OpenCV and required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "opencv-contrib-python", "numpy"])
            print("✓ OpenCV installed successfully.")
        except Exception as e:
            print(f"❌ Error installing OpenCV: {e}")
            print("\nYou can try installing it manually with:")
            print("pip install opencv-python opencv-contrib-python numpy")
            return
    
    # Create face data directory
    face_data_dir = "face_data"
    if not os.path.exists(face_data_dir):
        os.makedirs(face_data_dir)
        print(f"✓ Created face data directory: {face_data_dir}")
    else:
        print(f"✓ Face data directory already exists: {face_data_dir}")
    
    # Create samples directory
    samples_dir = os.path.join(face_data_dir, "samples")
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
        print(f"✓ Created face samples directory: {samples_dir}")
    else:
        print(f"✓ Face samples directory already exists: {samples_dir}")
    
    print("\n✅ Face recognition setup complete!")
    print("\nYou can now run the assistant with 'python run.py'")
    print("The first time you run it, you'll be prompted to train the face recognition model.")

if __name__ == "__main__":
    setup_face_recognition()

