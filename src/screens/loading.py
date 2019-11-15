"""
Loading screen.
"""
import time

import pygame

from src.screens.screen import Screen, Screens
from src.config import CONFIG


class LoadingScreen(Screen):

    def __init__(self):
        self.logo = pygame.image.load(CONFIG.BASE_FOLDER + 'images/logo.png')  # 45x12
        self.logo = pygame.transform.scale(self.logo, (5 * 45, 5 * 12,))

        self.pygame_logo = pygame.image.load(CONFIG.BASE_FOLDER + 'images/pygame_logo.gif')
        pygame_logo_size = self.pygame_logo.get_rect().size
        self.pygame_logo = pygame.transform.scale(self.pygame_logo, (pygame_logo_size[0] // 4, pygame_logo_size[1] // 4))

    def display(self, screen: pygame.Surface):
        screen.fill((100, 200, 150,))
        
        logo_size = self.logo.get_size()
        screen.blit(self.logo, (CONFIG.WINDOW_WIDTH // 2 - logo_size[0] // 2, CONFIG.WINDOW_HEIGHT // 2 - 150))
        screen.blit(self.pygame_logo, (50, CONFIG.WINDOW_HEIGHT - 100))
        
        pygame.display.update()
        pygame.display.flip()
        time.sleep(1.618)

        return Screens.MAIN_MENU
