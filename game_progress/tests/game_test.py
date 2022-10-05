""" Testing of Game class methods 
"""
from .. import Game


def test_init():
    """ A new game progress should return a negative value
    """
    game = Game()
    assert game.progress is False


def test_next_stage():
    """ Test next stage function of Game class
    """
    game = Game()
    game.next_stage()
    assert game.progress == 1


def test_reset():
    """ Test reset function of Game class
    """
    game = Game()
    game.next_stage()
    game.reset()
    new_game = Game()

    assert game.progress == new_game.progress
