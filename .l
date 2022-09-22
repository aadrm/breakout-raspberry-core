import RPi.GPIO as GPIO
import time
import urllib
import dbus,time
from subprocess import Popen

#GPIO Pins

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DoorMain = 23
Switch = 24
DoorLab = 13
DoorShip = 5
Ship = 12
ArduinoSmoke = 22

GPIO.setup(DoorMain, GPIO.IN)
GPIO.setup(Switch, GPIO.IN)
GPIO.setup(Ship, GPIO.IN)
GPIO.setup(DoorShip, GPIO.IN)

GPIO.setup(ArduinoSmoke, GPIO.OUT)
GPIO.output(ArduinoSmoke, 0)

DoorMainState = 0
DoorShipState = 0
ShipState = 0
SwitchState = 0
TimeStart = 0
TimeNow = 0
Timer = 0
SmokeEvent = 0
StatusTimer = time.time()

DoorMainEvent = 0
DoorShipEvent = 0
ShipEvent = 0

Movie = '/home/pi/Videos/EscapePod.mp4'
PCIP = '192.168.0.101'
PCPort = '14999'


def MainDoorCloses():
    global DoorMainEvent
    print('MainDoorCloses Funciotn Called')
    SwitchStateCheck = 0
    MainDoorCheck = 0
    for _ in range(50):
        time.sleep(0.01)
        MainDoorCheck += GPIO.input(DoorMain)
        SwitchStateCheck += GPIO.input(Switch)
    print(MainDoorCheck, SwitchStateCheck)
    if SwitchStateCheck == 0 and MainDoorCheck == 0:
        DoorMainEvent = 1
        print('MainDoorCloses Condition Pass: Game Start')
        TimeStart = time.time()
        httpReq("start")

def DoorShipOpens():
    global DoorShipEvent
    print("DoorShipOpens Funciton Call")
    DoorShipCheck = 0
    for _ in range(50):
        time.sleep(0.01)
        DoorShipCheck += GPIO.input(DoorShip)
    if DoorShipCheck > 49:
        DoorShipEvent = 1
        print('DorrShipOpens Condition Pass: CheckList Video')
        httpReq("checklist")

def ShipThrottleCloses():
    global ShipEvent
    print("ShipThrottleCloses Function Call")
    ShipCheck = 0
    for _ in range(50):
          time.sleep(0.01)
          ShipCheck += GPIO.input(Ship)
    print(ShipCheck)
    if ShipCheck == 0:
        print('ShipThrottleCloses Condition Pass: Play Video')
        ShipEvent = 1
        httpReq('endgame')
        omxc = Popen(['omxplayer', '--aspect-mode', 'fill', Movie])

def MainSwitchClose():
    print("SwitchClosed")

def MainSwitchOpen():
    global ShipState
    print("SwitchOpen")
    if ShipState == 2:
        Restart()

def Restart():

     print('Restart Call')

     global ShipEvent
     global DoorMainEvent
     global DoorShipEvent
     global TimeStart
     global TimeNow
     global Timers
     global SmokeEvent     
     
     GPIO.output(ArduinoSmoke, 0)
     ShipEvent = 0
     DoorMainEvent = 0
     DoorShipEvent = 0
     TimeStart = 0
     TimeNow = 0
     Timer = 0
     SmokeEvent = 0

def httpReq(command):
      try:
           url ="http://" + PCIP + ":" + PCPort + "/" + command
           print(url)
           response = urllib.urlopen(url).read()
           html = response
           time.sleep(0.02)
      except:
           print('Err')
           pass

while True:

    TimeNow = time.time()
    Timer = TimeNow - TimeStart
    DoorMainState = GPIO.input(DoorMain)
    DoorShipState = GPIO.input(DoorShip)
    ShipState = GPIO.input(Ship)
    SwitchState = GPIO.input(Switch)

    if TimeNow - StatusTimer > 5:
      print('-------------------')
      print('DoorMainState ', DoorMainState)
      print('DoorShipState ', DoorShipState)
      print('ShipState     ', ShipState)
      print('SwitchState   ', SwitchState)
      StatusTimer = time.time()

    if DoorMainState == 0 and SwitchState == 0 and DoorMainEvent == 0:
        MainDoorCloses()

    if Timer > 22 and DoorMainEvent == 1 and SmokeEvent == 0:
        time.sleep(22)
        print('smoke')
        print(Timer)
        GPIO.output(ArduinoSmoke, 1)
        SmokeEvent = 1

    if DoorShipState == 1 and DoorMainEvent == 1 and DoorShipEvent == 0:
        DoorShipOpens()

    if ShipState == 0 and ShipEvent == 0:
        ShipThrottleCloses()

    if SwitchState == 1 and ShipEvent == 1:
        Restart()
