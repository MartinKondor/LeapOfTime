"""
Game screen.
"""
import time

import pygame

from src.screens.screen import Screen, Screens
from src.config import CONFIG


class GameScreen(Screen):

    def __init__(self):
        pass

    def display(self, screen):
        return Screens.GAME
