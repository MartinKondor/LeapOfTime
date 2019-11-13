"""
Game screen.
"""
import time

import pygame
from pygame import locals as keys

from src.screens.screen import Screen, Screens
from src.config import CONFIG
from src.gfx.map import Map
from src.gameplay.player import Player


class GameScreen(Screen):

    def __init__(self):
        self.map = Map()
        self.player = Player()

        # Set player to the center of the map
        self.player.set_pos((len(self.map.layers[0][0]) * self.map.tileset.tile_size[1]) // 2,
                            (len(self.map.layers[0]) * self.map.tileset.tile_size[1]) // 2)

    def display(self, screen):
        self.map.display(self.player, screen)
        self.player.display(screen)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[keys.K_ESCAPE]:
            return Screens.MAIN_MENU
        return Screens.GAME
