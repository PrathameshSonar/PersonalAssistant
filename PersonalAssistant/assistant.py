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
from send_mail import send_mail
from inbox import get_inbox
from list_events import list_events
from create_event import create_event


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
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
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        return data

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12 :
        speak("Good Morning")

    elif hour>=12 and hour <18 :
        speak("Good Afternoon")

    elif hour>=18 and hour <20 :
        speak("Good Evening")
    else:
       speak("Good Night") 


def jarvis(data):
    
    
    if "how are you" in data:
        speak("I am fine")

    if "what time is it" in data:
        speak(ctime())

    if "exit" in data or "close" in data:
        speak('I feeling very sweet after meeting with you but you are going! i am very sad')
        exit()

    if "send mail" in data or "email" in data:
        speak('Enter a Email ID of User who u want to send mail')
        email_id = input('\n>>')
        speak('Tell a subject for mail : ')
        email_subject = recordAudio()
        speak('Tell a Email Body : ')
        email_body = recordAudio()
        send_mail(text=email_body,subject=email_subject,to_emails=[email_id])
        speak('Mail sent successfully')

    if "check for any new mail" in data:
        new_mail = get_inbox()
        speak('you have mail from ' + new_mail)

    if "schedule meeting" in data:
        speak('Enter date in DD/MM/YYYY format')
        dt_string = input('\nDate (DD/MM/YYYY): ')            
        
        speak('Enter time in HH:MM format')
        t = input('\nHH:MM : ')

        dt_string = dt_string + ' ' + t
        dt = datetime.datetime.strptime(dt_string,"%d/%m/%Y %H:%M")
        print(dt)

        currentDate = datetime.datetime.today()
        
        if dt <= currentDate:
            speak('Given date should be greater than todays date')
        else:
            speak('Tell a summary for meeting : ')
            summary = recordAudio()
            create_event(dt, summary)
            speak('Meeting scheduled successfully')
        

    if "check for any meeting scheduled" in data:
        events = list_events()
        for event in events:
           start = event['start'].get('dateTime', event['start'].get('date'))
           speak('you have meeting scheduled on ' + start)
           print(start, event['summary'])

    if "shutdown" in data:
            speak("shutting down")
            os.system('shutdown -s')

    
# initialization

greet()
speak("Hi Prathamesh, what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)
