"""
Class for active (glowing) tiles.
"""
import time

import pygame


class ActiveTiles:

    def __init__(self, objective_id: int, from_x_pos: float, to_x_pos: float, from_y_pos: float, to_y_pos: float,
                        glow_time=1, alpha_max: int=120, alpha_min: int=50, color: tuple=(4, 255, 0,)):
        self.objective_id = objective_id
        self.from_x_pos = from_x_pos
        self.to_x_pos = to_x_pos
        self.from_y_pos = from_y_pos
        self.to_y_pos = to_y_pos
        self.glow_time = glow_time
        self.alpha_max = alpha_max
        self.alpha_min = alpha_min
        self.increase_alpha = False
        self.color = list(color)
        self.current_alpha = self.alpha_max
        self.timer = time.time()

    def display(self, screen: pygame.Surface, player):
        player.max_speed = 7
        surface = pygame.Surface((abs(self.from_x_pos - self.to_x_pos), abs(self.from_y_pos - self.to_y_pos),))
        surface.set_alpha(self.current_alpha)
        surface.fill(self.color)
        screen.blit(surface, (self.from_x_pos - player.camera_x, self.from_y_pos - player.camera_y,))

        if (time.time() - self.timer) >= (self.glow_time / (self.alpha_max - self.alpha_min)):
            self.timer = time.time()

            if self.current_alpha >= self.alpha_max:
                self.increase_alpha = False
            elif self.current_alpha <= self.alpha_min:
                self.increase_alpha = True

            # Glow
            if self.increase_alpha:
                self.current_alpha += 1
            else:
                self.current_alpha -= 1
