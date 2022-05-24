from gpiozero import InputDevice, OutputDevice
import time
import logging
from datetime import datetime
from multiprocessing import Process, Queue

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('~/gateOp.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

isClose= 26
isOpen = 27

lift = 19
hik = 17
ac = 21

frontLS = 22
backLS = 23

crelay = 5
orelay = 6

stayOpenTime = 60

closingRelay = OutputDevice(crelay, active_high=False, initial_value=False)
openingRelay = OutputDevice(orelay, active_high=False, initial_value=False)
closeLimit = InputDevice(isClose, pull_up=False)
openLimit = InputDevice(isOpen, pull_up=False)
liftButton = InputDevice(lift, pull_up=True)
hikButton = InputDevice(hik, pull_up=False)
acButton = InputDevice(ac, pull_up=True)
frontLine = InputDevice(frontLS, pull_up=True)
backLine = InputDevice(backLS, pull_up=True)


def gateOpen():
    closingRelay.off()
    logger.debug("Closing relay OFF")
    openingRelay.on()
    logger.debug("Opening in progress")
    counter = 0
    try:
        while True:
            if openLimit.value:
                openingRelay.off()
                logger.debug("Opening completed")
                #print(f"Opening action took {counter} seconds")
                break



            counter += 1
            time.sleep(1)

    except Exception as e:
        print(e)

def gateClose():
    openingRelay.off()
    logger.debug("Opening relay OFF")
    closingRelay.on()
    logger.debug("Closign in progress")
    try:
        counter = 0
        while True:
            if closeLimit.value:
                closingRelay.off()
                logger.debug("Closing completed")
                #print(f"Closing action took {counter/2} seconds")
                break
            if checkRex():
                logger.debug("Closing interrupted")
                gateOpen()
                break
            if checkViolated():
                logger.debug("Closing interrupted")
                gateOpen()
                break



            counter += 1
            time.sleep(0.5)
    except Exception as e:
        print(e)



def checkRex():
    if liftButton.value:
        logger.debug("Lift master pressed")
        return True
    elif hikButton.value:
        logger.debug("Door station pressed")
        return True
    elif acButton.value:
        logger.debug("Access control pressed")
        return True
    else:
        return False
def checkViolated():
    if not frontLine.value:
        logger.debug("Front line sensor blocked")
        return True
    elif not backLine.value:
        logger.debug("Back line sensor blocked")
        return True
    else:
        return False

def main():
    time.sleep(5)
    try:
        gateTimer = 0
        while True:
            if openLimit.value:
                #print("Gate is open")
                gateTimer += 1
            if closeLimit.value:
                #print("Gate is closed")
                pass

            if gateTimer == stayOpenTime:
                if not checkViolated() and not checkRex():
                    logger.debug("Closing gate because not violated and timer expired")
                    gateClose()
                logger.debug("Timer reset")
                gateTimer = 0


            if checkRex() and not openLimit.value:
                gateOpen()
                logger.debug("Opening gate per request")

            time.sleep(1)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

