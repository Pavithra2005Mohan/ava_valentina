import speech_recognition as sr
import pyttsx3
import openai
import pyautogui
import face_recognition
import homeassistant

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty("rate", 170)

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

# Function to process commands
def process_command(command):
    if "open notepad" in command:
        pyautogui.hotkey("win", "r")
        pyautogui.typewrite("notepad")
        pyautogui.press("enter")
        speak("Opening Notepad")
    
    elif "control lights" in command:
        # Integrate with Home Assistant API
        speak("Turning on the lights")
        # Add Home Assistant API call here

    elif "who am i" in command:
        # Use face_recognition to identify user
        speak("Identifying you...")
        # Add face recognition logic here

    else:
        response = chat_with_gpt(command)
        speak(response)

# Function to chat with GPT-4
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are AVA, an advanced AI assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Activate AVA
def activate_ava():
    while True:
        command = listen()
        if command:
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            process_command(command)

# Run AVA
if __name__ == "__main__":
    activate_ava()
