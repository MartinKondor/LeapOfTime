"""
Class for active (glowing) tiles.
"""
import pygame


class ActiveTiles:

    def __init__(self, from_x_pos: float, to_x_pos: float, from_y_pos: float, to_y_pos: float, glow_time=0.5, from_color=(255, 255, 255,), to_color=(0, 0, 0,)):
        self.from_x_pos = from_x_pos
        self.to_x_pos = to_x_pos
        self.from_y_pos = from_y_pos
        self.to_y_pos = to_y_pos
        self.glow_time = glow_time
        self.from_color = from_color
        self.to_color = to_color

    def display(self, screen: pygame.Surface, player):
        # pygame.draw(pygame.rect.Rect(self.from_x_pos, self.from_y_pos, self.to_y_pos - self.to_x_pos, self.from_y_pos - self.to_y_pos,))
        pass
