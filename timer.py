from guizero import *
import datetime
import RPi.GPIO as GPIO

pause = False
seat1Open = 0
seat2Open = 0
seat3Open = 0
seat4Open = 0
openCount = 0

seat1Pin = 4
seat2Pin = 17
seat3Pin = 27
seat4Pin = 22

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
    timeLbl.set("00:00:00.00")
    seat1Time.set("LOCKED")
    seat2Time.set("LOCKED")
    seat3Time.set("LOCKED")
    seat4Time.set("LOCKED")
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
    timeLbl.set(custom_format(elapsed))
    if(seat1Open == 1):
        seat1Time.set(custom_format(elapsed))
        seat1Open = 2
    if(seat2Open == 1):
        seat2Time.set(custom_format(elapsed))
        seat2Open = 2
    if(seat3Open == 1):
        seat3Time.set(custom_format(elapsed))
        seat3Open = 2
    if(seat4Open == 1):
        seat4Time.set(custom_format(elapsed))
        seat4Open = 2
    if(openCount >= 4):
        stop()
    if(pause != True):
        timeLbl.after(10, update_time)

def readPin(pinnum):
    return GPIO.input(pinnum)
    return pinnum%2

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

app = App(title="Lockpick Village Timer", width=1280, height=1024, layout="grid")

title = Text(app, text="Lock Pick Village", size=40, font="Arial", color="darkblue", grid=[0,0])
timeLbl = Text(app, text="00:00:00.00", size=40, font="Arial", color="darkred", grid=[1,0])

seat1 = Text(app, text="Seat 1", size=40, font="Arial", color="darkblue", grid=[3,0])
seat2 = Text(app, text="Seat 2", size=40, font="Arial", color="darkblue", grid=[3,1])
seat1Time = Text(app, text="LOCKED", size=40, font="Arial", color="black", grid=[4,0])
seat2Time = Text(app, text="LOCKED", size=40, font="Arial", color="black", grid=[4,1])
seat3 = Text(app, text="Seat 3", size=40, font="Arial", color="darkblue", grid=[5,0])
seat4 = Text(app, text="Seat 4", size=40, font="Arial", color="darkblue", grid=[5,1])
seat3Time = Text(app, text="LOCKED", size=40, font="Arial", color="black", grid=[6,0])
seat4Time = Text(app, text="LOCKED", size=40, font="Arial", color="black", grid=[6,1])
btnStop = PushButton(app, text="Stop", command=stop, grid=[7,0])
btnReset = PushButton(app, text="Reset + Go", command=reset, grid=[7,1])

timeLbl.after(10, update_time)
start = datetime.datetime.utcnow()

app.display()

GPIO.cleanup()
