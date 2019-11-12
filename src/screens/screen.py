"""
Abstract screen object.
"""
from enum import Enum


class Screens(Enum):
    EXIT = 0
    LOADING = 1
    MAIN_MENU = 2
    SETTINGS = 3
    GAME = 4


class Screen:
    """
    Represents the abstract screen object
    """
    
    def display(self, screen):
        """
        :param screen: pygame.Surface
        :returns: Screen enum value
        """
        pass
