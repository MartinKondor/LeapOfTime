"""
Game screen.
"""
import time
from enum import Enum

import pygame

from src.gui import Button,  ButtonState
from src.screens.screen import Screen, Screens
from src.config import CONFIG
from src.gfx.map import Map
from src.gameplay.player import Player


class GameSubScreen(Enum):
    GAME = 0
    IN_GAME_MENU = 1


class GameScreen(Screen):

    def __init__(self):
        self.map = Map()
        self.player = Player()
        self.subscreen = GameSubScreen.GAME
        self.in_game_menu_bg = None

        # Set player to the center of the map
        self.player.set_pos((len(self.map.layers[0][0]) * self.map.tileset.tile_size[1]) // 2,
                            (len(self.map.layers[0]) * self.map.tileset.tile_size[1]) // 2)

        # In game menu elements
        button_margin = 50
        self.in_game_resume_button = Button(96, CONFIG.WINDOW_HEIGHT - 96 - 2 * button_margin, label='RESUME')
        self.in_game_exit_button = Button(96, CONFIG.WINDOW_HEIGHT - 96 - button_margin, label='EXIT')

    def display_game(self, screen):
        self.map.display(screen, self.player)
        self.player.display(screen, self.map)

        if pygame.key.get_pressed()[pygame.locals.K_ESCAPE]:

            # Save game screenshot as a background
            pygame.image.save(screen, CONFIG.BASE_FOLDER + '/images/screenshot.png')
            self.in_game_menu_bg = pygame.image.load(CONFIG.BASE_FOLDER + '/images/screenshot.png')
            self.in_game_menu_bg.set_alpha(150)
            self.subscreen = GameSubScreen.IN_GAME_MENU
            
        return Screens.GAME

    def display_in_game_menu(self, screen):
        screen.blit(self.in_game_menu_bg, (0, 0))
        self.in_game_resume_button.display(screen)
        self.in_game_exit_button.display(screen)

        if self.in_game_exit_button.state == ButtonState.RELEASED:
            return Screens.MAIN_MENU
        elif self.in_game_resume_button.state == ButtonState.RELEASED:
            self.subscreen = GameSubScreen.GAME
            return Screens.GAME
        return Screens.GAME

    def display(self, screen):
        if self.subscreen == GameSubScreen.GAME:
            return self.display_game(screen)
        else:
            return self.display_in_game_menu(screen)
        return Screens.GAME
