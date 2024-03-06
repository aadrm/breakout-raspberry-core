"""
Breakout Escape Room Spacelab Raspberry Pi Script

"""
import os
from time import sleep
from urllib.request import urlopen
from subprocess import Popen

try:
    import RPi.GPIO as GPIO
except ImportError:
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
THROTTLE_SIGNAL_TO_ARDUINO = 6
SMOKE_MACHINE = 22

DELAY_TO_SMOKE = 22

GPIO.setup(DOOR_MAIN, GPIO.IN)
GPIO.setup(STANDBY_SWITCH, GPIO.IN)
GPIO.setup(THROTTLE, GPIO.IN)
GPIO.setup(DOOR_SHIP, GPIO.IN)
GPIO.setup(SMOKE_MACHINE,  GPIO.OUT)
GPIO.setup(THROTTLE_SIGNAL_TO_ARDUINO, GPIO.OUT)
GPIO.output(THROTTLE_SIGNAL_TO_ARDUINO,  1)
GPIO.output(SMOKE_MACHINE,  0)



door_main_state = 0
door_ship_state = 0
standby_switch_state = 0
throttle = 0
door_main_event = 0
door_ship_event = 0
smoke_event = 0
end_of_game_event = 0

PATH_TO_SCRIPT = os.path.dirname(__file__)
PATH_TO_MEDIA = os.path.join(PATH_TO_SCRIPT, 'media')
PATH_TO_MOVIE = os.path.join(PATH_TO_MEDIA, 'video.mp4')
PATH_TO_IMAGE = os.path.join(PATH_TO_MEDIA, 'image.jpg')
HOUDINI_IP = '192.168.0.101'
HOUDINI_PORT = '14999'


def httpReq(command):
    url ="http://" + HOUDINI_IP + ":" + HOUDINI_PORT + "/" + command
    print(url)
    try:
        urlopen(url, timeout=2).read()
    except Exception:
        print('Err')


def debounce(pin: int) -> int:
    """ Debounces a GPIO input

    Args:
        pin (int): pin being debounced

    Returns:
        int: returns the value that was detected during most of the debouncing, \
            this value reflects the position of the switch
    """
    debounce_check = 0
    for _ in range(50):
        sleep(0.005)
        # using if to make it compatible with Mock.GPIO
        if GPIO.input(pin):
            debounce_check += 1

    position = 1 if debounce_check > 25 else 0
    return position


def print_sensor_status() -> None:
    game_sensors = {
        'door_main': 0,
        'door_ship': 0,
        'standby_switch': 0,
        'throttle': 0
    }
    game_sensors['door_main'] = GPIO.input(DOOR_MAIN)
    game_sensors['door_ship'] = GPIO.input(DOOR_SHIP)
    game_sensors['standby_switch'] = GPIO.input(STANDBY_SWITCH)
    game_sensors['throttle'] = GPIO.input(THROTTLE)
    print(game_sensors)


if __name__ == '__main__':
    game = Game()
    timer = Timer()
    print(game)
    print_sensor_status()
    print(PATH_TO_IMAGE)
    try:
        image_popen = Popen(['feh', '-Z', '-F', PATH_TO_IMAGE])
    except FileNotFoundError as e:
        print(e)

    while True:
        # Prevent looping too fast
        sleep(1)
        print_sensor_status()
        if not GPIO.input(DOOR_MAIN) \
            and not GPIO.input(STANDBY_SWITCH) \
            and game.progress == 0:
            if not debounce(DOOR_MAIN) and not debounce(STANDBY_SWITCH):
                timer.new_datum()
                print("Main door closed")
                game.next_stage()
                print(game)
                httpReq("start")

        if game.progress == 1:
            time_to_smoke = DELAY_TO_SMOKE - timer.time_passed()
            print(f'time to smoke: {time_to_smoke}')

        if timer.time_passed() > DELAY_TO_SMOKE and game.progress == 1:
            GPIO.output(SMOKE_MACHINE,  1)
            game.next_stage()
            print(game)

        if GPIO.input(DOOR_SHIP) == 1 and game.progress == 2:
            if debounce(DOOR_SHIP):
                game.next_stage()
                print(game)
                httpReq("checklist")

        if game.progress == 3 and not GPIO.input(THROTTLE):
            if debounce(THROTTLE) is False:
                game.next_stage()
                httpReq('endgame')
                GPIO.output(THROTTLE_SIGNAL_TO_ARDUINO,  0)
                try:
                    video_popen = Popen(['cvlc', '-f', PATH_TO_MOVIE])
                except Exception as e:
                    print(e)

        if GPIO.input(STANDBY_SWITCH) == 1 and game.progress > 3:
            if debounce(STANDBY_SWITCH):
                print('Restart Call')
                game.reset()
                print(game)
                GPIO.output(SMOKE_MACHINE,  0)
                GPIO.output(THROTTLE_SIGNAL_TO_ARDUINO,  1)
