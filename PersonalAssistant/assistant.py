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
import pyttsx3
import webbrowser
from send_mail import send_mail
from inbox import get_inbox
from list_events import list_events
from create_event import create_event
from file_manager import getName
from file_manager import setName
from subprocess import call
import subprocess
import psutil
from tkinter import *
from tkinter import simpledialog
from urllib.request import urlopen
import json


#from finan import get_data
#from finance import get_stock


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

window = Tk()
window.configure(bg="black")
window.geometry("640x640")
window.maxsize(640, 640)
window.iconbitmap("jss.png")

global labelString1
global labelString2


labelString1 = StringVar()
labelString2 = StringVar()


def speak(audioString):
    engine.say(audioString)
    print(audioString)
    engine.runAndWait()


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        labelString1.set("Listening...")
        window.update()
        print("Listening...")
        audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        data = ""
        try:
            labelString1.set("Recognizing...")
            window.update()
            data = r.recognize_google(audio)
            print("You said: " + data)

        except sr.UnknownValueError:
            labelString1.set("I am not getting what you have said")
            window.update()
            speak("I am not getting what you have said")

        except sr.RequestError as e:
            labelString1.set("I am not getting what you have said")
            window.update()
            speak("I am not getting what you have said")

        return data.lower()


def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        window.update()
        speak("Good Morning")

    elif hour >= 12 and hour < 18:
        window.update()
        speak("Good Afternoon")

    elif hour >= 18 and hour < 20:
        window.update()
        speak("Good Evening")

    else:
        window.update()
        speak("Good Night")


def jarvis():
    time.sleep(10)
    greet()
    labelString2.set("Hi " + getName() + ", what can I do for you?")
    window.update()
    speak("Hi " + getName() + ", what can I do for you?")
    while True:
        # btn1.configure(bg='grey')

        data = recordAudio()

        if "what time is it" in data:
            labelString2.set(ctime())
            window.update()
            speak(ctime())

        elif "exit" in data or "close" in data or "goodbye" in data:
            labelString2.set(
                "I feeling very sweet after meeting with you but you are going! i am very sad")
            window.update()
            speak(
                "I feeling very sweet after meeting with you but you are going! i am very sad")
            exit()

        elif "send mail" in data or "email" in data:
            labelString2.set(
                "Enter a Email ID of User who u want to send mail")
            window.update()
            speak("Enter a Email ID of User who u want to send mail")

            email_id = simpledialog.askstring(
                "Input", "Enter Email ID", parent=window)
            if email_id is not None:
                print(email_id)
                labelString2.set("Tell a subject for mail : ")
                window.update()
                speak("Tell a subject for mail : ")
                email_subject = recordAudio()

                labelString2.set("Tell a Email Body : ")
                window.update()
                speak("Tell a Email Body : ")
                email_body = recordAudio()

                send_mail(text=email_body, subject=email_subject,
                          to_emails=[email_id])
                labelString2.set("Mail sent successfully")
                window.update()
                speak("Mail sent successfully")

            else:
                labelString2.set("You haven't entered Email ID yet")
                window.update()
                speak("You haven't entered Email ID yet")

        elif "check for any new mail" in data:
            new_mail = get_inbox()
            labelString2.set("you have mail from " + new_mail)
            window.update()
            speak("you have mail from " + new_mail)

        elif "schedule meeting" in data:
            speak("Enter date in DD/MM/YYYY format")
            dt_string = simpledialog.askstring(
                "Input", "Enter date in DD/MM/YYYY format", parent=window)

            speak("Enter time in HH:MM format")
            t = simpledialog.askstring(
                "Input", "Enter time in HH:MM format", parent=window)

            dt_string = dt_string + " " + t
            dt = datetime.datetime.strptime(dt_string, "%d/%m/%Y %H:%M")
            print(dt)

            currentDate = datetime.datetime.today()

            if dt <= currentDate:
                labelString2.set(
                    "Given date should be greater than todays date")
                window.update()
                speak("Given date should be greater than todays date")
            else:
                labelString2.set("Tell a summary for meeting : ")
                window.update()
                speak("Tell a summary for meeting : ")
                summary = recordAudio()
                create_event(dt, summary)
                labelString2.set("Meeting scheduled successfully")
                window.update()
                speak("Meeting scheduled successfully")

        elif "check for any meeting scheduled" in data:
            events = list_events()
            for event in events:
                start = event["start"].get(
                    "dateTime", event["start"].get("date"))
                labelString2.set("you have meeting scheduled on " + start)
                window.update()
                speak("you have meeting scheduled on " + start)
                print(start, event["summary"])

        elif "shutdown" in data:
            labelString2.set(
                "Hold On a Sec ! Your system is on its way to shut down")
            window.update()
            speak("Hold On a Sec ! Your system is on its way to shut down")
            os.system("shutdown -s")

        elif "hibernate" in data or "sleep" in data:
            labelString2.set("Hibernating..")
            window.update()
            speak("Hibernating..")
            os.system("shutdown.exe /h")

        elif "change name" in data or "name change" in data:
            labelString2.set("Tell a new name")
            window.update()
            speak("Tell a new name")
            name = recordAudio()
            if name:
                setName(name)
                labelString2.set(f"okay, i will remember that {name}")
                window.update()
                speak(f"okay, i will remember that {name}")

        elif "open youtube" in data or "open video online" in data:
            webbrowser.open("www.youtube.com")
            labelString2.set("Opening Youtube")
            window.update()
            speak("opening youtube")

        elif "open github" in data:
            webbrowser.open("https://www.github.com")
            labelString2.set("Opening Github")
            window.update()
            speak("opening github")

        elif "open facebook" in data:
            webbrowser.open("https://www.facebook.com")
            labelString2.set("Opening Facebook")
            window.update()
            speak("opening facebook")

        elif "open instagram" in data:
            webbrowser.open("https://www.instagram.com")
            labelString2.set("Opening Instagram")
            window.update()
            speak("opening instagram")

        elif "open google" in data:
            webbrowser.open("https://www.google.com")
            labelString2.set("Opening Google")
            window.update()
            speak("opening google")

        elif "open yahoo" in data:
            webbrowser.open("https://www.yahoo.com")
            labelString2.set("Opening Yahoo")
            window.update()
            speak("opening yahoo")

        elif "open amazon" in data or "shop online" in data:
            webbrowser.open("https://www.amazon.com")
            labelString2.set("Opening Amazon")
            window.update()
            speak("opening amazon")

        elif "open flipkart" in data:
            webbrowser.open("https://www.flipkart.com")
            labelString2.set("Opening Flipkart")
            window.update()
            speak("opening flipkart")

        elif "what\"s up" in data or "how are you" in data:
            stMsgs = ["Just doing my thing!", "I am fine!", "Nice!",
                      "I am nice and full of energy", "i am okey ! How are you"]
            ans_q = random.choice(stMsgs)
            labelString2.set(ans_q)
            window.update()
            speak(ans_q)
            user_reply = recordAudio()
            if "fine" in user_reply or "ok" in user_reply:
                labelString2.set("Okay")
                window.update()
                speak("okay..")
            elif "not" in user_reply or "sad" in user_reply or "upset" in user_reply:
                labelString2.set("Oh Sorry..")
                window.update()
                speak("oh sorry..")

        elif "who are you" in data or "about you" in data or "your details" in data:
            labelString2.set("I am ALICE, Your Virtual Assistant")
            window.update()
            speak("I am ALICE, Your Virtual Assistant")

        elif "hey alice" in data or "hello alice" in data:
            name = getName()
            labelString2.set("Hello " + name + " How may i help you")
            window.update()
            speak("Hello " + name + " How may i help you")

        elif "open calculator" in data or "calculator" in data:
            labelString2.set("Opening calculator")
            window.update()
            speak("opening calculator")
            call(["calc.exe"])

        elif "open notepad" in data or "notepad" in data:
            labelString2.set("Opening Notepad")
            window.update()
            speak("opening notepad")
            call(["notepad.exe"])

        elif "search for" in data and "youtube" not in data:
            search_term = data.split("for")[-1]
            url = f"https://google.com/search?q={search_term}"
            webbrowser.get().open(url)
            labelString2.set(
                f"Here is what I found for {search_term} on google")
            window.update()
            speak(f"Here is what I found for {search_term} on google")

        elif " on youtube" in data:
            search_term = data.split("on")[-1]
            url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.get().open(url)
            labelString2.set(f"Here is what I found for {search_term}")
            window.update()
            speak(f"Here is what I found for {search_term}")

        elif "don't listen" in data or "stop listening" in data:
            labelString2.set(
                "for how much time you want to stop assistant from listening commands")
            window.update()
            speak("for how much time you want to stop assistant from listening commands")
            a = int(recordAudio())
            labelString2.set("Sleeping..")
            window.update()
            speak("Sleeping..")
            time.sleep(a)

        elif "locate " in data:
            search_term = data.split(" ")[-1]
            url = f"https://www.google.com/maps/place/{search_term}"
            webbrowser.get().open(url)
            labelString2.set(
                f"Here is what I found for {search_term} on google map")
            window.update()
            speak(f"Here is what I found for {search_term} on google map")

        elif "check battery status" in data:
            battery = psutil.sensors_battery()
            plugged = battery.power_plugged
            percent = str(battery.percent)
            plugged = "Plugged In" if plugged else "Not Plugged In"
            labelString2.set(percent+'% available and system is '+plugged)
            window.update()
            speak(percent+'% available and system is '+plugged)

        elif 'show news' in data:
            try:
                jsonObj = urlopen('http://newsapi.org/v2/top-headlines?'
                                  'country=us&'
                                  'apiKey=ef7399983f78497983b23c2da7e0efcc')

                data = json.load(jsonObj)
                i = 1
                labelString2.set('Here are some top worldwide news : ')
                window.update()
                speak('here are some top worldwide news ')
                print('''=============== TIMES OF INDIA ============''' + '\n')

                for item in data['articles']:
                    if(i > 3):
                        break
                    else:
                        print(str(i) + '. ' + item['title'] + '\n')
                        print(item['description'] + '\n')
                        speak(str(i) + '. ' + item['title'] + '\n')
                        i += 1
                        
            except Exception as e:
                print(str(e))

        # if "show yahoo stocks":
            # get_data("UU.L")
        # if "compare stocks" in data:
            # get_stocks()


def update(ind):
    frame = frames[ind % 1]
    ind += 1
    label.configure(image=frame)
    window.after(100, update, ind)


# initialization

label2 = Label(window, textvariable=labelString2, bg='black')
label2.config(font=("Courier", 12), fg='white')
labelString2.set('.....')
label2.pack()

label1 = Label(window, textvariable=labelString1, bg='black')
label1.config(font=("Courier", 20), fg='white')
labelString1.set('Welcome')
label1.pack()

frames = [PhotoImage(file='assistant.png')]
window.title('ALICE')

label = Label(window, width=500, height=500)
label.pack()
window.after(0, update, 0)

#entry = Entry(window)
# entry.pack()

#btn = Button(text='SUBMIT', width=20, command = getTextfieldContent, bg='grey', fg='white')
#btn.config(font=("Courier", 12))
# btn.pack()


#btn1 = Button(text='SPEAK', width=20, command=jarvis, bg='black', fg='white')
#btn1.config(font=("Courier", 12))
# btn1.pack()

#btn2 = Button(text='EXIT', width=20, command=window.destroy, bg='black', fg="white")
#btn2.config(font=("Courier", 12))
# btn2.pack()

jarvis()
window.mainloop()
