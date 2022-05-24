import RPi.GPIO as GPIO
from time import sleep




isClose = 26
isOpen = 27
crelay = 5
orelay = 6
lights = 20
lift = 17
hik = 18
ac = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(crelay, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(orelay, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(lights, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(isClose, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(isOpen, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lift, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(hik, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ac, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def closeRelayOn():
    GPIO.output(crelay, 0)

def closeRelayOff():
    GPIO.output(crelay, 1)

def openRelayOn():
    GPIO.output(orelay, 0)

def openRelayOff():
    GPIO.output(orelay, 1)

def lightsOn():
    print("Lights are on")
    try:
        GPIO.output(lights, 0)
    except Exception as e:
        print(e)

def lightsOff():
    print("Lights are off")
    try:
        GPIO.output(lights, 1)
    except Exception as e:
        print(e)
def checkRex():
    if GPIO.input(lift):
        print("Lift master is pressed")
    elif GPIO.input(hik):
        print("Door station is pressed")
    elif GPIO.input(ac):
        print("Access keypad is pressed")



def close_gate():
    counter = 0
    while True:
        closeRelayOn()
        if GPIO.input(isClose):
            closeRelayOff()
            print(counter)
            break
        sleep(1)
        counter += 1
#    closeRelayOn()
#    sleep(30)
#    closeRelayOff()
def open_gate():
    counter = 0
    while True:
        openRelayOn()
        if GPIO.input(isOpen):
            openRelayOff()
            print(counter)
            break
        sleep(1)
        counter += 1
#    openRelayOn()
#    sleep(30)
#    openRelayOff()



#GPIO.output(lights, 0)
try:
    while True:
        print(GPIO.input(26))
        print(GPIO.input(27))
        if GPIO.input(26):
            print("Gate is Closed")
        if GPIO.input(27):
            print("Gate is Open")
        command = input("open/close?")
        if command == "open":
            try:
                open_gate()
            except Exception as e:
                print(e)

        elif command == "close":
            try:
                close_gate()
            except Exception as e:
                print(e)
        elif command == "on":
            try:
                lightsOn()
            except Exception as e:
                print(e)
        elif command == "off":
            try:
                lightsOff()
            except Exception as e:
                print(e)
        elif command == "rex":
            checkRex()
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    #GPIO.output(lights, 1)
    GPIO.cleanup()


