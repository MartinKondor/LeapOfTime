"""
GamePlay class for managing the gameplay.
"""
import time

import pygame

from src.config import CONFIG


class GamePlay:

    def __init__(self):

        # Setup the current level
        if CONFIG.CURRENT_LEVEL == '0':
            from src.gameplay.levels.level_0 import Level0
            self.level = Level0()
        elif CONFIG.CURRENT_LEVEL == '1':
            from src.gameplay.levels.level_1 import Level1
            self.level = Level1()
        else:
            # Set player to the center of the map
            self.level.player.set_pos(self.level.map.layer_size[0] / 2 - self.level.player.body.width / 4, \
                                self.level.map.layer_size[1] / 2 - self.level.player.body.height / 2)

        # Load the HUD
        self.can_show_hud = True
        self.hud_elements = []
        self.hud_width = 64
        self.hud_height = 32
        self.hud_game_time_sprite = CONFIG.hud_font.render(self.level.game_time, 1, (50, 53, 63,))
        hud_img = pygame.image.load(CONFIG.BASE_FOLDER + 'gfx/hud/hud.png').convert()
        # hud_img.set_alpha(220)
        hud_img.set_colorkey((0, 255, 0,))

        for x in range(3):
            hud_img.set_clip(pygame.Rect(x * self.hud_width, 0, self.hud_width, self.hud_height))
            img = hud_img.subsurface(hud_img.get_clip())
            self.hud_elements.append(pygame.transform.scale(img, (128, 64,)))

        # Scretch the center to fill any screen width
        self.hud_width = 128
        self.hud_height = 64
        self.hud_elements[1] = pygame.transform.scale(self.hud_elements[1], (CONFIG.WINDOW_WIDTH - 2 * self.hud_width, self.hud_height,))

        # Intro variables
        self.intro_timer = time.time()
        self.intro_time = 2
        self.intro_shown = CONFIG.DEBUG  # Do not show intro on debug mode

    def display(self, screen: pygame.Surface):
        if not self.intro_shown:
            screen.fill(CONFIG.BG_COLOR)

            level_str = 'LEVEL ' + str(int(CONFIG.CURRENT_LEVEL) + 1)
            screen.blit(CONFIG.readable_font.render(level_str, 1, (240, 249, 255,)),
                        (CONFIG.WINDOW_WIDTH / 2 - (len(level_str) * CONFIG.CHARACTER_SIZE / 4), CONFIG.WINDOW_HEIGHT / 2,))

            screen.blit(CONFIG.readable_font.render(self.level.game_time, 1, (240, 249, 255,)),
                        (CONFIG.WINDOW_WIDTH / 2 - (len(level_str) * CONFIG.CHARACTER_SIZE / 4), CONFIG.WINDOW_HEIGHT / 2 + 2 * CONFIG.CHARACTER_SIZE,))

            if time.time() - self.intro_timer >= self.intro_time:
                self.intro_shown = True
        else:
            self.level.display(screen)

            # Display HUD
            if self.can_show_hud:
                screen.blit(self.hud_elements[0], (0, CONFIG.WINDOW_HEIGHT - self.hud_height,))
                screen.blit(self.hud_elements[1], (self.hud_width, CONFIG.WINDOW_HEIGHT - self.hud_height,))
                screen.blit(self.hud_elements[2], (CONFIG.WINDOW_WIDTH - self.hud_width, CONFIG.WINDOW_HEIGHT - self.hud_height,))
                screen.blit(self.hud_game_time_sprite, (CONFIG.WINDOW_WIDTH - len(self.level.game_time) * 13 + 32, CONFIG.WINDOW_HEIGHT - 32,))
