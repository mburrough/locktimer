# Lock Timer v8
# 1080p edition
# DEC 1 2024
# (C) 2017-2024 Matt Burrough
# 
# For 3D Printed KIK Timers
# Updated for guizero 1.5.0

##Uncomment to test on Fake RPi Python lib
#import sys
#import fake_rpi
#sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
#sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
#sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

from guizero import *
import datetime
import RPi.GPIO as GPIO

logFilePath = "locktimerlog.csv"
logFile = True
verbose = False

seat1Pin = 27
seat2Pin = 22
seat3Pin = 4
seat4Pin = 17

seat1StopPin = 25
seat2StopPin = 5
seat3StopPin = 6
seat4StopPin = 12

seat1GoPin = 24
seat2GoPin = 16
seat3GoPin = 18
seat4GoPin = 23

#states:
# 0 = stopped / reset
# 1 = running (locked)
# 2 = opened / stopped
seat1State = 0
seat2State = 0
seat3State = 0
seat4State = 0
start1 = 0
start2 = 0
start3 = 0
start4 = 0

buttonTriggered = 0
inputTriggered = 0

def custom_format(td):
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    seconds += td.microseconds / 1e6
    return '{:02d}:{:02d}:{:05.2f}'.format(hours, minutes, seconds)

def begin1():
    global start1
    global seat1State
    global logFile
    global verbose
    
    seat1Time.value = "00:00:00.00"
    seat1Time.text_color = "green"
    seat1State = 1
    start1 = datetime.datetime.utcnow()
    if(verbose):
        print("Seat 1,BEGIN,", start1, file=logFile)

def begin2():
    global start2
    global seat2State
    global logFile
    global verbose
    
    seat2Time.value = "00:00:00.00"
    seat2Time.text_color = "green"
    seat2State = 1
    start2 = datetime.datetime.utcnow()
    if(verbose):
        print("Seat 2,BEGIN,", start2, file=logFile)

def begin3():
    global start3
    global seat3State
    global logFile
    global verbose
    
    seat3Time.value = "00:00:00.00"
    seat3Time.text_color = "green"
    seat3State = 1
    start3 = datetime.datetime.utcnow()
    if(verbose):
        print("Seat 3,BEGIN,", start3, file=logFile)

def begin4():
    global start4
    global seat4State
    global logFile
    global verbose
    
    seat4Time.value = "00:00:00.00"
    seat4Time.text_color = "green"
    seat4State = 1
    start4 = datetime.datetime.utcnow()
    if(verbose):
        print("Seat 4,BEGIN,", start4, file=logFile)

    
def reset1():
    global start1
    global seat1State
    global logFile
    global verbose
    
    seat1Time.value = "00:00:00.00"
    seat1Time.text_color = "red"
    seat1State = 0
    if(verbose):
        print("Seat 1,RESET,", datetime.datetime.utcnow(), file=logFile)
    
def reset2():
    global start2
    global seat2State
    global logFile
    global verbose
    
    seat2Time.value = "00:00:00.00"
    seat2Time.text_color = "red"
    seat2State = 0
    if(verbose):
        print("Seat 2,RESET,", datetime.datetime.utcnow(), file=logFile)

def reset3():
    global start3
    global seat3State
    global logFile
    global verbose
    seat3Time.value = "00:00:00.00"
    seat3Time.text_color = "red"
    seat3State = 0
    if(verbose):
        print("Seat 3,RESET,", datetime.datetime.utcnow(), file=logFile)

def reset4():
    global start4
    global seat4State
    global logFile
    global verbose
    
    seat4Time.value = "00:00:00.00"
    seat4Time.text_color = "red"
    seat4State = 0
    if(verbose):
        print("Seat 4,RESET,", datetime.datetime.utcnow(), file=logFile)

def update_time():
    global seat1State
    global seat2State
    global seat3State
    global seat4State
    now = datetime.datetime.utcnow()
    checkLocks()
    
    if(seat1State == 1):
        seat1Time.value = custom_format(now - start1)

    if(seat2State == 1):
        seat2Time.value = custom_format(now - start2)

    if(seat3State == 1):
        seat3Time.value = custom_format(now - start3)

    if(seat4State == 1):
        seat4Time.value = custom_format(now - start4)
    
    checkButtons()
    
    
def readPin(pinnum):
    return GPIO.input(pinnum)

def configButton(pinnum):
    print("Setting up button on pin ", pinnum)
    GPIO.setup(pinnum, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def configInput(pinnum):
    print("Setting up input on pin ", pinnum)
    GPIO.setup(pinnum, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
def checkLocks():
    global seat1State
    global seat2State
    global seat3State
    global seat4State
    global logFile
    
    if(readPin(seat1Pin) == inputTriggered and seat1State == 1):
        seat1State = 2
        seat1Time.text_color = "blue"
        print("Seat 1,OPEN,", datetime.datetime.utcnow(),",", seat1Time.value, file=logFile)
        logFile.flush()
    if(readPin(seat2Pin) == inputTriggered and seat2State == 1):
        seat2State = 2
        seat2Time.text_color = "blue"
        print("Seat 2,OPEN,", datetime.datetime.utcnow(),",", seat2Time.value, file=logFile)
        logFile.flush()
    if(readPin(seat3Pin) == inputTriggered and seat3State == 1):
        seat3State = 2
        seat3Time.text_color = "blue"
        print("Seat 3,OPEN,", datetime.datetime.utcnow(),",", seat3Time.value, file=logFile)
        logFile.flush()
    if(readPin(seat4Pin) == inputTriggered and seat4State == 1):
        seat4State = 2
        seat4Time.text_color = "blue"        
        print("Seat 4,OPEN,", datetime.datetime.utcnow(),",", seat4Time.value, file=logFile)
        logFile.flush()


def checkButtons():
    if(readPin(seat1StopPin) == buttonTriggered):
        reset1()
    if(readPin(seat2StopPin) == buttonTriggered):
        reset2()
    if(readPin(seat3StopPin) == buttonTriggered):
        reset3()
    if(readPin(seat4StopPin) == buttonTriggered):
        reset4()
        
    if(readPin(seat1GoPin) == buttonTriggered):
        begin1()
    if(readPin(seat2GoPin) == buttonTriggered):
        begin2()
    if(readPin(seat3GoPin) == buttonTriggered):
        begin3()
    if(readPin(seat4GoPin) == buttonTriggered):
        begin4()
    

# Main
GPIO.setmode(GPIO.BCM)
logFile = open(logFilePath, "a")

print("N/A,GAME START,", datetime.datetime.utcnow(), file=logFile)
logFile.flush()

configInput(seat1Pin)
configInput(seat2Pin)
configInput(seat3Pin)
configInput(seat4Pin)
configButton(seat1StopPin)
configButton(seat2StopPin)
configButton(seat3StopPin)
configButton(seat4StopPin)
configButton(seat1GoPin)
configButton(seat2GoPin)
configButton(seat3GoPin)
configButton(seat4GoPin)

app = App(title="Lockpick Village Timer", width=1920, height=1080)

title = Text(app, text="Lockpick Village Timed Challenge", size=64, font="Arial", color="darkblue")
box = Box(app, layout="grid")

seat1 = Text(box, text="Seat 1", size=48, font="Arial", color="darkblue", grid=[0,0], align="top")
seat2 = Text(box, text="Seat 2", size=48, font="Arial", color="darkblue", grid=[2,0], align="top")
seat1Time = Text(box, text="00:00:00.00", size=48, font="Arial", color="black", grid=[0,1], align="top")
space1 = Text(box, text=" ", size=48, font="Arial", color="black", grid=[1,1], align="top")
seat2Time = Text(box, text="00:00:00.00", size=48, font="Arial", color="black", grid=[2,1], align="top")
space2 = Text(box, text=" ", size=48, font="Arial", color="black", grid=[0,2], align="top")
seat3 = Text(box, text="Seat 3", size=48, font="Arial", color="darkblue", grid=[0,3], align="top")
seat4 = Text(box, text="Seat 4", size=48, font="Arial", color="darkblue", grid=[2,3], align="top")
seat3Time = Text(box, text="00:00:00.00", size=48, font="Arial", color="black", grid=[0,4], align="top")
space3 = Text(box, text=" ", size=48, font="Arial", color="black", grid=[1,4], align="top")
seat4Time = Text(box, text="00:00:00.00", size=48, font="Arial", color="black", grid=[2,4], align="top")


title.repeat(10, update_time)

start1 = datetime.datetime.utcnow()
start2 = datetime.datetime.utcnow()
start3 = datetime.datetime.utcnow()
start4 = datetime.datetime.utcnow()

app.display()


print("N/A,GAME SHUTDOWN,", datetime.datetime.utcnow(), file=logFile)

logFile.flush()
logFile.close()

GPIO.cleanup()
