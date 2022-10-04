import os
import time
import urllib
from subprocess import Popen

try:
    import RPi.GPIO as GPIO
except Exception:
    import Mock.GPIO as GPIO

from game_progress import Game
from timer import Timer

#GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DOOR_MAIN = 23
STANDBY_SWITCH = 24
DOOR_SHIP = 5
THROTTLE = 12
SMOKE_MACHINE = 22

GPIO.setup(DOOR_MAIN, GPIO.IN)
GPIO.setup(STANDBY_SWITCH, GPIO.IN)
GPIO.setup(THROTTLE, GPIO.IN)
GPIO.setup(DOOR_SHIP, GPIO.IN)
GPIO.setup(SMOKE_MACHINE,  GPIO.OUT)
GPIO.output(SMOKE_MACHINE,  0)


game_sensors = {
    'door_main': 0,
    'door_ship': 0,
    'standby_switch': 0,
    'throttle': 0
}

door_main_state = 0
door_ship_state = 0
standby_switch_state = 0
throttle = 0
door_main_event = 0
door_ship_event = 0
smoke_event = 0
end_of_game_event = 0

PATH_TO_SCRIPT = os.path.dirname(__file__) + '/'
REL_PATH_TO_MEDIA = 'media/'
ESCAPE_POD_VIDEO_FILE = 'video.mp4'
HANGAR_IMAGE_FILE = 'image.jpg'
HOUDINI_IP = '192.168.0.101'
HOUDINI_PORT = '14999'

def main_door_closes(game: Game, timer: Timer, sensors: dict):
    SwitchStateCheck = 0
    MainDoorCheck = 0
    for _ in range(50):
        time.sleep(0.01)
        MainDoorCheck += GPIO.input(DOOR_MAIN)
        SwitchStateCheck += GPIO.input(STANDBY_SWITCH)
    if SwitchStateCheck < 10 and MainDoorCheck < 10:
        game.next_stage() 
        print(game)
        httpReq("start")

def DoorShipOpens():
    
    print("DoorShipOpens Funciton Call")
    DoorShipCheck = 0
    for _ in range(50):
        time.sleep(0.01)
        DoorShipCheck += GPIO.input(DOOR_SHIP)
    if DoorShipCheck > 49:
        door_ship_event = 1
        print('DorrShipOpens Condition Pass: CheckList Video')
        httpReq("checklist")

def ShipThrottleCloses():
    globalend_of_game_event 
    print("ShipThrottleCloses Function Call")
    ShipCheck = 0
    for _ in range(50):
          time.sleep(0.01)
          ShipCheck += GPIO.input(SHIP)
    print(ShipCheck)
    if ShipCheck == 0:
        print('ShipThrottleCloses Condition Pass: Play Video')
        end_of_game_event = 1
        httpReq('endgame')
        omxc = Popen(['omxplayer', '--aspect-mode', 'fill', Movie])

def MainSwitchClose():
    print("SwitchClosed")

def MainSwitchOpen():
    globalship_state 
    print("SwitchOpen")
    if game_progress == 2:
        Restart()

def Restart():

     print('Restart Call')

     global end_of_game_event 
     global door_main_event 
     global door_ship_event 
     global time_start 
     global TimeNow
     global Timers
     global smoke_event     
     
     GPIO.output(SMOKE_MACHINE,  0)
     end_of_game_event = 0
     door_main_event = 0
     door_ship_event = 0
     time_start = 0
     TimeNow = 0
     timer = 0
     smoke_event = 0

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

def print_sensor_status(sersors):
    print('------------------------')
    print(sensors)


if __name__ == '__main__':

    game = Game()
    timer = Timer()
    print(game)
    print(game_sensors)
    while True:
        game_sensors['door_main'] = GPIO.input(DOOR_MAIN)
        game_sensors['door_ship'] = GPIO.input(DOOR_SHIP)
        game_sensors['standby_switch'] = GPIO.input(STANDBY_SWITCH)
        game_sensors['throttle'] = GPIO.input(THROTTLE)


        if game_sensors['door_main'] == 0 \
                and sensors['standby_switch'] == 0 \
                and game.progress == 0:
            main_door_closes(game)

        if timer.time_passed() > 22 and door_main_event == 1 and smoke_event == 0:
            print('smoke')
            print()
            GPIO.output(SMOKE_MACHINE,  1)
            smoke_event = 1

        if door_ship_state == 1 and door_main_event == 1 and door_ship_event == 0:
            DoorShipOpens()

        if game.progress == 1 and end_of_game_event == 0:
            ShipThrottleCloses()

        if game_sensors['standby_switch']== 1 and end_of_game_event == 1:
            Restart()
