import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("The python-dotenv package is not installed. Installing it now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

def setup_huggingface_api_key():
    """
    Set up the Hugging Face API key as an environment variable and save it to a .env file.
    """
    print("\n=== Hugging Face API Key Setup ===\n")
    print("Note: Many Hugging Face models work without an API key, so this step is optional.")
    print("If you have a Hugging Face account, you can get your API key from: https://huggingface.co/settings/tokens")

    # Load existing environment variables from .env if it exists
    try:
        load_dotenv(override=True)
    except Exception as e:
        print(f"Warning: Could not load existing environment variables: {e}")

    # Check if the API key is already set
    existing_key = os.getenv("HUGGINGFACE_API_KEY")
    if existing_key:
        print("✓ Hugging Face API key is already set.")
        change_key = input("Do you want to change it? (y/n): ").strip().lower()
        if change_key != 'y':
            return

    # Get the API key from the user
    print("\nIf you don't have an API key, just press Enter to skip. The assistant will use public models.")
    api_key = input("\nEnter your Hugging Face API key (or press Enter to skip): ").strip()

    if not api_key:
        print("No API key provided. The assistant will use public models only.")
        # Remove the key from environment if it exists
        if "HUGGINGFACE_API_KEY" in os.environ:
            del os.environ["HUGGINGFACE_API_KEY"]
        
        # Update the .env file without the key
        update_env_file("HUGGINGFACE_API_KEY", None)
        return

    # Save API key to the environment variable and .env file
    try:
        os.environ["HUGGINGFACE_API_KEY"] = api_key
        update_env_file("HUGGINGFACE_API_KEY", api_key)
        print("\n✅ Hugging Face API key has been set successfully!")
    except Exception as e:
        print(f"\n❌ Error saving API key: {e}")
        return

def update_env_file(key, value):
    """Update a specific key in the .env file without affecting other keys."""
    env_file = ".env"
    
    # Read existing content
    lines = []
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()
    
    # Filter out the key we're updating
    lines = [line for line in lines if not line.startswith(f"{key}=")]
    
    # Add the new key-value pair if value is not None
    if value is not None:
        lines.append(f"{key}={value}\n")
    
    # Write back to the file
    with open(env_file, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    setup_huggingface_api_key()

