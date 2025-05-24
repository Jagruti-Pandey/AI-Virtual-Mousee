import speech_recognition as sr
import pyautogui
import subprocess
import webbrowser
import datetime
import os
import time
import pyttsx3
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet

# ----------- CONFIGURATION -----------

# File paths
python_files = {
    "volume": r"C:\Users\Jagruti pandey\.android\bootstrap\volume control.py",
    "click": r"C:\Users\Jagruti pandey\.android\bootstrap\click.py",
    "tracking": r"C:\Users\Jagruti pandey\.android\bootstrap\eye tracking.py"
}
html_file = r"C:\Users\Jagruti pandey\.android\bootstrap\index.html"

# Password encryption
key_file = "secret.key"
password_file = "password.enc"
log_file = "log.txt"

# ----------- SETUP -----------

# Auto-start setup (Windows only)
def add_to_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script_path = os.path.realpath(__file__)
    bat_path = os.path.join(startup_path, "VoiceAssistant.bat")
    with open(bat_path, "w") as bat_file:
        bat_file.write(f'start "" python "{script_path}"\n')

# Generate encryption key
def generate_key():
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, 'wb') as key_out:
            key_out.write(key)

# Load encryption key
def load_key():
    return open(key_file, 'rb').read()

# Encrypt and save password
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    with open(password_file, 'wb') as enc_file:
        enc_file.write(encrypted)

# Decrypt password
def decrypt_password():
    key = load_key()
    fernet = Fernet(key)
    with open(password_file, 'rb') as enc_file:
        encrypted = enc_file.read()
    return fernet.decrypt(encrypted).decode()

def voice_password_check():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say the secret password to continue.")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        voice_input = r.recognize_google(audio).lower().strip()
        print(f"You said: {voice_input}")
        if voice_input == "virtual":  # You can change this to any phrase
            speak("Voice password accepted. Welcome.")
            return True
        else:
            speak("Incorrect voice password. Access denied.")
            return False
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error.")
    return False


# Logging function
def log_command(command):
    with open(log_file, 'a') as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {command}\n")

# ----------- ASSISTANT FUNCTIONS -----------

engine = pyttsx3.init()

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def recognize_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower().strip()
        print(f"You said: {command}")
        log_command(command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error. Please check your connection.")
    return ""

def execute_command(command):
    if "scroll up" in command:
        pyautogui.scroll(500)
        speak("Scrolling up.")
    elif "scroll down" in command:
        pyautogui.scroll(-500)
        speak("Scrolling down.")
    elif "left click" in command:
        pyautogui.click()
        speak("Left click done.")
    elif "right click" in command:
        pyautogui.click(button='right')
        speak("Right click done.")
    elif "open explorer" in command or "open windows explorer" in command:
        subprocess.Popen("explorer")
        speak("Opening File Explorer.")
    elif "open visual studio code" in command:
        subprocess.Popen("code")
        speak("Opening Visual Studio Code.")
    elif "open camera" in command:
        subprocess.Popen("start microsoft.windows.camera:", shell=True)
        speak("Opening camera.")
    elif "open calculator" in command:
        subprocess.Popen("calc")
        speak("Opening calculator.")
    elif "open calendar" in command:
        subprocess.Popen("start outlookcal:", shell=True)
        speak("Opening calendar.")
    elif "current time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "run volume" in command:
        file_path = python_files["volume"]
        if os.path.exists(file_path):
            subprocess.Popen([sys.executable, file_path])
            speak("Running volume.")
        else:
            speak("Sorry, file one was not found.")
    elif "run click" in command:
        file_path = python_files["click"]
        if os.path.exists(file_path):
            subprocess.Popen([sys.executable, file_path])
            speak("Running click.")
        else:
            speak("Sorry, file two was not found.")
    elif "run tracking" in command:
        file_path = python_files["tracking"]
        if os.path.exists(file_path):
            subprocess.Popen([sys.executable, file_path])
            speak("Running tracking.")
        else:
            speak("Sorry, file three was not found.")
    elif "run html file" in command or "open html file" in command:
        if os.path.exists(html_file):
            webbrowser.open(f"file:///{html_file}")
            speak("Opening HTML file.")
        else:
            speak("HTML file not found.")
    elif "exit" in command or "stop listening" in command:
        speak("bye!")
        exit()
    else:
        speak("I didn't recognize that command.")

# ----------- MAIN FUNCTION -----------

if __name__ == "__main__":
    try:
        add_to_startup()
        generate_key()

        # 👇 Only this voice-based virtual password will be used
        if not voice_password_check():
            sys.exit()

        while True:
            command = recognize_command()
            if command:
                execute_command(command)
            time.sleep(0.5)

    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred. Check your setup.")