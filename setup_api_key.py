import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("The python-dotenv package is not installed. Installing it now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

def setup_openai_api_key():
    """
    Set up the OpenAI API key as an environment variable and save it to a .env file.
    """
    print("\n=== OpenAI API Key Setup ===\n")

    # Load existing environment variables from .env if it exists
    try:
        load_dotenv(override=True)
    except Exception as e:
        print(f"Warning: Could not load existing environment variables: {e}")

    # Check if the API key is already set
    existing_key = os.getenv("OPENAI_API_KEY")
    if existing_key:
        print("✓ OpenAI API key is already set.")
        change_key = input("Do you want to change it? (y/n): ").strip().lower()
        if change_key != 'y':
            return

    # Get the API key from the user
    print("\nYou can get your API key from: https://platform.openai.com/api-keys")
    api_key = input("\nEnter your OpenAI API key: ").strip()

    if not api_key:
        print("No API key provided. Exiting.")
        return

    # Validate the API key format (basic check)
    if not (api_key.startswith("sk-") and len(api_key) > 20):
        print("\n⚠️ Warning: The API key format doesn't look right. OpenAI API keys typically start with 'sk-'")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return

    # Save API key to the environment variable and .env file
    try:
        os.environ["OPENAI_API_KEY"] = api_key
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("\n✅ OpenAI API key has been set successfully!")
    except Exception as e:
        print(f"\n❌ Error saving API key: {e}")
        return

    print("\nTo make it permanent, add it to your system environment variables:")
    print("---------------------------------------------------------------")
    print("🔹 Windows (PowerShell):")
    print(f'   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "{api_key}", "User")')
    print("🔹 Mac/Linux (Bash/Zsh):")
    print(f'   echo \'export OPENAI_API_KEY="{api_key}"\' >> ~/.bashrc && source ~/.bashrc')
    print("\nNow restart your assistant with: python run.py")

if __name__ == "__main__":
    setup_openai_api_key()

