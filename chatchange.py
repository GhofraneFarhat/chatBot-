import speech_recognition as sr
import webbrowser

# Initialize recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Define the trigger word to open the website
trigger_word = "prof"

# Define the URL you want to open
url = "https://ensi.rnu.tn/"

# Loop forever
while True:
    # Use the microphone to listen for speech
    with mic as source:
        print("tkallem...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # Use speech recognition to convert speech to text
    try:
        text = r.recognize_google(audio, language='fr-FR')
        print("You said: {}".format(text))
    except sr.UnknownValueError:
        print("masme3tekch.")
        continue

    # If the trigger word is detected, open the website
    if trigger_word in text:
        print("Ouvrir la page web...")
        webbrowser.open(url)
