# Lock Timer v6
# 1080p edition
# DEC 5 2023
# (C) 2017-2023 Matt Burrough
# 
# For revised stands with NC switches
# Updated for guizero 1.5.0

from guizero import *
import datetime
import RPi.GPIO as GPIO

seat1Pin = 4
seat2Pin = 17
seat3Pin = 27
seat4Pin = 22

pause = False
seat1Open = 0
seat2Open = 0
seat3Open = 0
seat4Open = 0
openCount = 0

start = datetime.datetime.utcnow()

def custom_format(td):
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    seconds += td.microseconds / 1e6
    return '{:02d}:{:02d}:{:05.2f}'.format(hours, minutes, seconds)

def stop():
    global pause
    pause = True

def reset():
    global pause
    global start
    global seat1Open
    global seat2Open
    global seat3Open
    global seat4Open
    global openCount
    timeLbl.value = "00:00:00.00"
    seat1Time.value = "LOCKED"
    seat2Time.value = "LOCKED"
    seat3Time.value = "LOCKED"
    seat4Time.value = "LOCKED"
    seat1Open = 0
    seat2Open = 0
    seat3Open = 0
    seat4Open = 0
    openCount = 0
    pause = False
    start = datetime.datetime.utcnow()
    timeLbl.after(10, update_time)

def update_time():
    global seat1Open
    global seat2Open
    global seat3Open
    global seat4Open
    now = datetime.datetime.utcnow()
    checkLocks()
    elapsed = now - start
    timeLbl.value = custom_format(elapsed)
    if(seat1Open == 1):
        seat1Time.value = custom_format(elapsed)
        seat1Open = 2
    if(seat2Open == 1):
        seat2Time.value = custom_format(elapsed)
        seat2Open = 2
    if(seat3Open == 1):
        seat3Time.value = custom_format(elapsed)
        seat3Open = 2
    if(seat4Open == 1):
        seat4Time.value = custom_format(elapsed)
        seat4Open = 2
    if(openCount >= 4):
        stop()
    if(pause != True):
        timeLbl.after(10, update_time)

def readPin(pinnum):
    return GPIO.input(pinnum)

def configPin(pinnum):
    total = pinnum + 1
    GPIO.setup(pinnum, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
def checkLocks():
    global seat1Open
    global seat2Open
    global seat3Open
    global seat4Open
    global openCount
    if(readPin(seat1Pin) == 1 and seat1Open < 1):
        openCount += 1
        seat1Open = 1
    if(readPin(seat2Pin) == 1 and seat2Open < 1):
        openCount += 1
        seat2Open = 1
    if(readPin(seat3Pin) == 1 and seat3Open < 1):
        openCount += 1
        seat3Open = 1
    if(readPin(seat4Pin) == 1 and seat4Open < 1):
        openCount += 1
        seat4Open = 1                        

# Main
GPIO.setmode(GPIO.BCM)
configPin(seat1Pin)
configPin(seat2Pin)
configPin(seat3Pin)
configPin(seat4Pin)

app = App(title="Lockpick Village Timer", width=1920, height=1080)

title = Text(app, text="Lockpick Village Timed Challenge", size=64, font="Arial", color="darkblue")
timeLbl = Text(app, text="00:00:00.00", size=72, font="Arial", color="darkred")
box = Box(app, layout="grid")

seat1 = Text(box, text="Seat 1", size=48, font="Arial", color="darkblue", grid=[0,0], align="top")
seat2 = Text(box, text="Seat 2", size=48, font="Arial", color="darkblue", grid=[2,0], align="top")
seat1Time = Text(box, text="LOCKED", size=48, font="Arial", color="black", grid=[0,1], align="top")
space1 = Text(box, text=" ", size=48, font="Arial", color="black", grid=[1,1], align="top")
seat2Time = Text(box, text="LOCKED", size=48, font="Arial", color="black", grid=[2,1], align="top")
space2 = Text(box, text=" ", size=48, font="Arial", color="black", grid=[0,2], align="top")
seat3 = Text(box, text="Seat 3", size=48, font="Arial", color="darkblue", grid=[0,3], align="top")
seat4 = Text(box, text="Seat 4", size=48, font="Arial", color="darkblue", grid=[2,3], align="top")
seat3Time = Text(box, text="LOCKED", size=48, font="Arial", color="black", grid=[0,4], align="top")
space3 = Text(box, text=" ", size=48, font="Arial", color="black", grid=[1,4], align="top")
seat4Time = Text(box, text="LOCKED", size=48, font="Arial", color="black", grid=[2,4], align="top")
btnStop = PushButton(box, text="Stop", command=stop, grid=[0,5], align="top")
btnReset = PushButton(box, text="Reset + Go", command=reset, grid=[2,5], align="top")

timeLbl.after(10, update_time)
start = datetime.datetime.utcnow()

app.display()

GPIO.cleanup()
