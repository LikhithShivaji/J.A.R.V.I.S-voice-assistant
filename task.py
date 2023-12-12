import datetime
from speak import Say
from GoogleNews import GoogleNews
import pywhatkit as pwt
from bs4 import BeautifulSoup
import requests
import pyfirmata
from pyfirmata import Arduino,util
import time
import os
from listen import Listen
import pyautogui

apikey="449A97-G5HJ95UEG3"
googlenews=GoogleNews()
board = Arduino('COM3')
led_pin = 12
# fan_pin=7
enable_pin = board.get_pin('d:9:p')  # PWM pin for speed control
in1_pin = board.get_pin('d:8:o')    # Direction pin 1
in2_pin = board.get_pin('d:10:o')   # Direction pin 2


#----------------------------------------------------------------------------------
it = util.Iterator(board)
it.start()
board.digital[led_pin].mode = pyfirmata.OUTPUT

#----------------------------------------------------------------------------------
commands = {
    'start fan': (1, 1),  # Direction: Forward, Speed: Maximum
    'stop fan': (0, 0),   # Direction: Stop, Speed: 0
    'reverse fan': (0, 1) # Direction: Reverse, Speed: Maximum
}

def control_fan(query):
    if query in commands:
        direction, speed = commands[query]
        in1_pin.write(direction)
        in2_pin.write(1 - direction)
        enable_pin.write(speed)
        Say("Turning the fan on")
    elif query in commands=='stop the fan':
        Say("Turning the fan off")

#----------------------------------------------------------------------------------




def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        Say("Good Morning sir!")
    elif hour>=12 and hour<16:
        Say("Good afternoon sir! Hope you are with a wonderful plan")
    else:
        Say("Good evening sir! Hope your day was worth the time, is there anything i can help you with?")

# Defining the functions------------------------------------------------

def Time():
    time=datetime.datetime.now().strftime("%H:%M")
    Say(time)

def Date():
    date=datetime.date.today()
    Say(date)

def Day():
    day=datetime.datetime.now().strftime("%A")
    Say(day)

def control_light(query):
    if 'turn on' in query:
        board.digital[led_pin].write(1) 
        Say('Light turned on')
    elif 'turn off' in query:
        board.digital[led_pin].write(0) 
        Say('Light turned off')
    else:
        print('Invalid command')

# def control_fan(query):
#     if 'fan on' in query:
#         board.digital[fan_pin].write(1) 
#         Say('Fan turned on')
#     elif 'fan off' in query:
#         board.digital[fan_pin].write(0) 
#         Say('Fan turned off')
#     else:
#         print('Invalid command')

#-------------------------------------------------------------------------

def NonInputExecution(query):

    query=str(query)

    if "time" in query:
        Time()

    elif "date" in query:
        Date()

    elif "day" in query:
        Day()
    
def InputExecution(tag,query):

    if "wikipedia" in tag:
        name=str(query).replace("who is","").replace("about","").replace("information","").replace("wikipedia","")
        import wikipedia
        result=wikipedia.summary(name)
        Say(result)

    elif "google" in tag:
        query=str(query).replace("google","").replace("search","")
        pwt.search(query)

   
    elif 'news' in tag:
        Say("Fetching the latest information for you sir")
        googlenews.get_news(query)
        googlenews.result()
        a=googlenews.gettext()
        print(*a[1:3])
        Say(a[1:5])    

    elif 'calculate' in tag:
        from Calculatenum import WolfRamAlpha
        from Calculatenum import Calc
        query=query.replace("calculate","")
        query=query.replace("jarvis","")
        Calc(query)

    elif 'song' in tag:
        #try pywinauto method for elsewhere
        pwt.playonyt(query)

    elif 'temperature' in tag:
        search="temperature in hassan"
        url=f"https://www.google.com/search?q={query}"
        r=requests.get(url)
        data=BeautifulSoup(r.text,"html.parser")
        temp=data.find("div", class_ = "BNeawe").text
        print(f"current {query} is {temp}")
        Say(f"current{query} is {temp}")

    elif 'weather' in tag:
        search="weather in hassan"
        url=f"https://www.google.com/search?q={query}"
        r=requests.get(url)
        data=BeautifulSoup(r.text,"html.parser")
        temp=data.find("div", class_ = "BNeawe").text
        Say(f"current{query} is {temp}")

    elif 'light' in tag:
        control_light(query)

    elif 'fan' in tag:
        control_fan(query)

    elif "remember that" in tag:
        Say("What do you want me to remember sir?")
        message=Listen()
        rememberMessage = message.replace("remember that","")
        Say("You told me to remember that "+rememberMessage)
        remember = open("Remember.txt","a")
        remember.write(rememberMessage)
        remember.close()

    elif "what do you remember" in tag:
        remember = open("Remember.txt","r")
        Say("Sir, you told me to remember that " + remember.read())


    elif "pause" in tag:
        pyautogui.press("k")
        Say("video paused")
    elif "play" in tag:
        pyautogui.press("k")
        Say("video played")    
    elif "mute" in tag:
        pyautogui.press("m")
        Say("video muted")


    elif "screenshot" in tag:
        image = pyautogui.screenshot()
        image.save("ss.jpg")
        Say("Screen shot captured sir!")

    elif "open" in tag:   
        Say("What application do you want me to open sir?")
        message=Listen()
        message1 = message.replace("open","")
        message2 = message1.replace("jarvis","")
        pyautogui.press("super")
        pyautogui.typewrite(message2)
        pyautogui.sleep(2)
        pyautogui.press("enter")
        Say("Opening the application for you sir!")

    elif "translate" in tag:
        from Translator import translategl
        # query = query.replace("jarvis","")
        # query1 = query.replace("translate","")
        translategl()

    elif "volume up" in tag:
        from keyboard import volumeup
        Say("Turning volume up sir!")
        volumeup()

    elif "volume down" in tag:
        from keyboard import volumedown
        Say("Turning volume down sir!")
        volumedown()

    elif "shutdown" in tag:
        Say("Shutting down the system sir! Anything unsaved will be deleted. Are you sure you want to shut down?")
        shutdown = Listen()
        if shutdown == "yes":
            os.system("shutdown /s /t 1")