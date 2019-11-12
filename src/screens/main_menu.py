"""
Main menu screen.
"""
import pygame

from src.config import CONFIG
from src.gui import Button, ButtonState
from src.screens.screen import Screen, Screens


class MainMenuScreen(Screen):
    
    def __init__(self):
        self.logo = pygame.image.load(CONFIG.BASE_FOLDER + 'images/logo.png')  # 45x12
        self.logo = pygame.transform.scale(self.logo, (5 * 45, 5 * 12,))
        self.logo_size = self.logo.get_rect().size

        button_margin = 50
        self.new_game_button = Button(96, CONFIG.WINDOW_HEIGHT - 96 - 2 * button_margin, 'NEW GAME')
        self.settings_button = Button(96, CONFIG.WINDOW_HEIGHT - 96 - button_margin, 'SETTINGS')
        self.exit_button = Button(96, CONFIG.WINDOW_HEIGHT - 96, 'EXIT')

    def display(self, screen):
        screen.blit(self.logo, (CONFIG.WINDOW_WIDTH - 1.5 * self.logo_size[0], self.logo_size[1] // 2,))
        self.new_game_button.display(screen)
        self.settings_button.display(screen)
        self.exit_button.display(screen)

        # Check buttons
        if self.exit_button.state == ButtonState.RELEASED:
            return Screens.EXIT
        if self.new_game_button.state == ButtonState.RELEASED:
            return Screens.GAME
        if self.settings_button.state == ButtonState.RELEASED:
            return Screens.SETTINGS
        return Screens.MAIN_MENU
