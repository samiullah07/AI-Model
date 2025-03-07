import subprocess
import sys

def check_and_install_opencv():
    """Check if OpenCV is installed and install it if needed."""
    try:
        import cv2
        print("OpenCV is already installed.")
        return True
    except ImportError:
        print("OpenCV is not installed. Installing now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "opencv-contrib-python"])
            print("OpenCV installed successfully.")
            return True
        except Exception as e:
            print(f"Error installing OpenCV: {e}")
            print("You can try installing it manually with:")
            print("pip install opencv-python opencv-contrib-python")
            return False

if __name__ == "__main__":
    check_and_install_opencv()

