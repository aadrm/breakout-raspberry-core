""" Escape Room Raspberry
"""
import os

from game_progress import Game
from gadgets import RpiInput

PATH_TO_SCRIPT = os.path.dirname(__file__) + '/'
REL_PATH_TO_MEDIA = 'media/'
ESCAPE_POD_VIDEO_FILE = 'video.mp4'
HANGAR_IMAGE_FILE = 'image.jpg'


my_sensors = {
    'door_main': 0,
    'door_ship': 0,
    'standby_switch': 0,
    'throttle': 0
}

def print_sensor_status(sensors: dict):
    print('------------------------')
    print(sensors)

if __name__ == '__main__':
    game = Game()

    print(game)
    game.next_stage()
    print(game)
    game.next_stage()
    print(game)
    game.next_stage()
    print(game)
    game.reset()
    print(game)
    print_sensor_status(my_sensors)

    door = RpiInput(5)

