# 1 Player Lock Timer v6a
# 720p edition
# DEC 5 2023
# (C) 2017-2023 Matt Burrough
# 
# For revised stands with NC switches
# Updated for guizero 1.5.0

from guizero import *
import datetime
from datetime import timedelta
import RPi.GPIO as GPIO

seat1Pin = 4
maxTime = 5

pause = False
seat1Open = 0
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
    global openCount
    timeLbl.value = "00:00:00.00"
    seat1Time.value = "LOCKED"
    seat1Open = 0
    openCount = 0
    pause = False
    start = datetime.datetime.utcnow()
    timeLbl.after(10, update_time)

def update_time():
    global seat1Open
    global maxTime
    now = datetime.datetime.utcnow()
    checkLocks()
    elapsed = now - start
    timeLbl.value = custom_format(elapsed)
    if(seat1Open == 1):
        seat1Time.value = "OPEN!"
        seat1Open = 2
    if(openCount >= 1):
        stop()
    if(pause != True):
        timeLbl.after(10, update_time)
    if(now - timedelta(minutes=maxTime) >= start):
        seat1Time.value = "TIME'S UP!"
        stop()

def readPin(pinnum):
    return GPIO.input(pinnum)

def configPin(pinnum):
    total = pinnum + 1
    GPIO.setup(pinnum, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
def checkLocks():
    global seat1Open
    global openCount
    if(readPin(seat1Pin) == 1 and seat1Open < 1):
        openCount += 1
        seat1Open = 1                      

# Main
GPIO.setmode(GPIO.BCM)
configPin(seat1Pin)

app = App(title="Lockpick Village Timer", width=1280, height=720)

title = Text(app, text="Lockpick Village Timed Challenge", size=64, font="Arial", color="darkblue")
spacer = Text(app, text=" ", size=48, font="Arial", color="darkblue")
timeLbl = Text(app, text="00:00:00.00", size=72, font="Arial", color="darkred")
spacer2 = Text(app, text=" ", size=48, font="Arial", color="darkblue")
seat1Time = Text(app, text="LOCKED", size=72, font="Arial", color="black")
box = Box(app, layout="grid")
btnStop = PushButton(box, text="Stop", command=stop, grid=[0,0])
spacer3 = Text(box, text=" ", size=48, font="Arial", color="darkblue", grid=[1,0])
btnReset = PushButton(box, text="Reset + Go", command=reset, grid=[2,0])

timeLbl.after(10, update_time)
start = datetime.datetime.utcnow()

app.display()

GPIO.cleanup()
