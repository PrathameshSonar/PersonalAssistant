#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
import playsound
import random
from time import ctime
import time
import datetime
import os
from gtts import gTTS
import webbrowser
from send_mail import send_mail
from inbox import get_inbox
from list_events import list_events
from create_event import create_event
from file_manager import getName
from file_manager import setName
from subprocess import call
import subprocess
#from finan import get_data
#from finance import get_stock


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang="en")
    r = random.randint(1, 20000000)
    audio_file = "audio" + str(r) + ".mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    #os.system("mpg321 audio.mp3")
    os.remove(audio_file)


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        data = ""
        try:

            data = r.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

        return data.lower()


def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")

    elif hour >= 18 and hour < 20:
        speak("Good Evening")
    else:
        speak("Good Night")


def jarvis(data):

    if "what time is it" in data:
        speak(ctime())

    elif "exit" in data or "close" in data or "goodbye" in data:
        speak(
            "I feeling very sweet after meeting with you but you are going! i am very sad")
        exit()

    elif "send mail" in data or "email" in data:
        speak("Enter a Email ID of User who u want to send mail")
        email_id = input("\n>>")
        speak("Tell a subject for mail : ")
        email_subject = recordAudio()
        speak("Tell a Email Body : ")
        email_body = recordAudio()
        send_mail(text=email_body, subject=email_subject, to_emails=[email_id])
        speak("Mail sent successfully")

    elif "check for any new mail" in data:
        new_mail = get_inbox()
        speak("you have mail from " + new_mail)

    elif "schedule meeting" in data:
        speak("Enter date in DD/MM/YYYY format")
        dt_string = input("\nDate (DD/MM/YYYY): ")

        speak("Enter time in HH:MM format")
        t = input("\nHH:MM : ")

        dt_string = dt_string + " " + t
        dt = datetime.datetime.strptime(dt_string, "%d/%m/%Y %H:%M")
        print(dt)

        currentDate = datetime.datetime.today()

        if dt <= currentDate:
            speak("Given date should be greater than todays date")
        else:
            speak("Tell a summary for meeting : ")
            summary = recordAudio()
            create_event(dt, summary)
            speak("Meeting scheduled successfully")

    elif "check for any meeting scheduled" in data:
        events = list_events()
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            speak("you have meeting scheduled on " + start)
            print(start, event["summary"])

    elif "shutdown" in data:
        speak("Hold On a Sec ! Your system is on its way to shut down")
        os.system("shutdown -s")

    elif "hibernate" in data or "sleep" in data:
        speak("Hibernating")
        os.system("shutdown.exe /h")

    elif "change name" in data or "name change" in data:
        speak("tell a new name")
        name = recordAudio()
        if name:
            setName(name)
            speak(f"okay, i will remember that {name}")

    elif "open youtube" in data or "open video online" in data:
        webbrowser.open("www.youtube.com")
        speak("opening youtube")

    elif "open github" in data:
        webbrowser.open("https://www.github.com")
        speak("opening github")

    elif "open facebook" in data:
        webbrowser.open("https://www.facebook.com")
        speak("opening facebook")

    elif "open instagram" in data:
        webbrowser.open("https://www.instagram.com")
        speak("opening instagram")

    elif "open google" in data:
        webbrowser.open("https://www.google.com")
        speak("opening google")

    elif "open yahoo" in data:
        webbrowser.open("https://www.yahoo.com")
        speak("opening yahoo")

    elif "open amazon" in data or "shop online" in data:
        webbrowser.open("https://www.amazon.com")
        speak("opening amazon")

    elif "open flipkart" in data:
        webbrowser.open("https://www.flipkart.com")
        speak("opening flipkart")

    elif "what\"s up" in data or "how are you" in data:
        stMsgs = ["Just doing my thing!", "I am fine!", "Nice!",
                  "I am nice and full of energy", "i am okey ! How are you"]
        ans_q = random.choice(stMsgs)
        speak(ans_q)
        user_reply = recordAudio()
        if "fine" in user_reply or "okay" in user_reply:
            speak("okay..")
        elif "not" in user_reply or "sad" in user_reply or "upset" in user_reply:
            speak("oh sorry..")

    elif "who are you" in data or "about you" in data or "your details" in data:
        speak("i am your assistant")

    elif "hey buddy" in data or "hello buddy" in data:
        name = getName()
        speak("Hello " + name + " How may i help you")

    elif "open calculator" in data or "calculator" in data:
        speak("opening calculator")
        call(["calc.exe"])

    elif "open notepad" in data or "notepad" in data:
        speak("opening notepad")
        call(["notepad.exe"])

    elif "search for" in data and "youtube" not in data:
        search_term = data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f"Here is what I found for {search_term} on google")

    elif "youtube" in data:
        search_term = data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f"Here is what I found for {search_term}")

    elif "don't listen" in data or "stop listening" in data:
        speak("for how much time you want to stop assistant from listening commands")
        a = int(recordAudio())
        time.sleep(a)

    elif "locate " in data:
        search_term = data.split(" ")[-1]
        print(search_term)
        url = f"https://www.google.com/maps/place/{search_term}"
        webbrowser.get().open(url)
        speak(f"Here is what I found for {search_term} on google map")
        


    # if "show yahoo stocks":
        # get_data("UU.L")
    # if "compare stocks" in data:
        # get_stocks()
# initialization
greet()
speak("Hi " + getName() + ", what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)
