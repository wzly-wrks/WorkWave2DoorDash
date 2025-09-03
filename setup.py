import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("Error installing requirements. Please install manually using:")
        print("pip install -r requirements.txt")
        return False
    return True

if __name__ == "__main__":
    if install_requirements():
        print("Setup complete! You can now run the converter using:")
        if os.name == 'nt':  # Windows
            print("run_converter.bat")
        else:  # Unix/Linux/Mac
            print("python workwave_to_doordash.py")