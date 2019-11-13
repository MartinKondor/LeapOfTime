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

        # Set player to the center of the map
        self.player.x_pos = (len(self.map.layers[0][0]) * self.map.tileset.tile_size[1]) // 2
        self.player.y_pos = (len(self.map.layers[0]) * self.map.tileset.tile_size[1]) // 2
        self.player.camera_x = self.player.x_pos
        self.player.camera_y = self.player.y_pos

    def display(self, screen):
        self.map.display(self.player, screen)
        self.player.display(screen)
        return Screens.GAME
