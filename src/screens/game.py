"""
Game screen.
"""
import time

import pygame

from src.screens.screen import Screen, Screens
from src.config import CONFIG
from src.gameplay.map import Map
from src.gameplay.player import Player


class GameScreen(Screen):

    def __init__(self):
        self.map = Map()
        self.player = Player()

    def display(self, screen):
        self.map.display(screen)
        self.player.display(screen)
        return Screens.GAME
