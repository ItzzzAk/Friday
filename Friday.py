import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import re

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning !!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!!")
    else:
        speak("Good Evening !!")
    speak("This is Friday. How may I help you today?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(":Listening ......")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)

    try:
        print(":Recognizing ......")
        query = r.recognize_google(audio, language="en-us")
        print(f"User said : {query}\n")
    except Exception as e:
        print(e)
        print(":none")
        return "None"
    return query

def sendEmail(to, subject, content):
    try:
        sender_email = "kalelamol08@gmail.com"
        sender_password = "flrn bbkm mamn dgau"  # Replace with your app password
        
        # Prepare email message
        message = f"Subject: {subject}\n\n{content}"
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)  # Enable debugging output
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, message)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I am not able to send the email at the moment.")

def cleanEmailAddress(address):
    # Replace common verbal descriptions with their actual symbols
    address = address.lower()
    address = address.replace("at the rate", "@")
    address = address.replace("dot", ".")
    address = address.replace(" ", "")  # Remove spaces
    return address

def extractEmailAddress(query):
    # Clean the query to handle verbal descriptions
    cleaned_query = cleanEmailAddress(query)
    # Use regex to find an email address in the cleaned query
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, cleaned_query)
    if match:
        return match.group(0)
    return None

def getEmailAddress():
    speak("Please say the full email address.")
    while True:
        email_address = takeCommand().lower()
        cleaned_email = cleanEmailAddress(email_address)
        extracted_email = extractEmailAddress(cleaned_email)
        if extracted_email:
            return extracted_email
        else:
            speak("I didn't catch that. Can you please repeat the email address?")

def getSubject():
    speak("What is the subject of the email?")
    while True:
        subject = takeCommand()
        if subject:
            return subject
        else:
            speak("I didn't catch that. Can you please repeat the subject?")



if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")
            speak("Opening YouTube")
            print("Opening YouTube")

        elif "open google" in query:
            webbrowser.open("google.com")
            speak("Opening Google")
            print("Opening Google")

        elif "play song" in query:
            music_dir = "E:\\songs"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
            speak("Playing music")
            print("Playing music")

        elif "close song" in query:
            os.system("taskkill /im wmplayer.exe /f")
            speak("Closing music")
            print("Closing music")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            print(f"The time is {strTime}")

        elif "open notepad" in query:
            codepath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(codepath)
            speak("Opening Notepad")
            print("Opening Notepad")

        elif "close notepad" in query:
            os.system("taskkill /im notepad.exe /f")
            speak("Closing Notepad")
            print("Closing Notepad")

        elif "send email" in query:
            speak("Tell me the email address to which you want to send the email.")
            email_address = getEmailAddress()
            
            if email_address:
                speak("What is the subject of the email?")
                subject = getSubject()
                
                if subject:
                    speak("What should I say in the email?")
                    content = takeCommand()
                    sendEmail(email_address, subject, content)
                else:
                    speak("I couldn't understand the subject. Please try again.")
            else:
                speak("I couldn't find a valid email address. Please try again.")

        elif "sleep" in query:
            speak("Quitting")
            exit()
