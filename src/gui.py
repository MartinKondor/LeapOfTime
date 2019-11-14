"""
GUI elements and utilites.
"""
from enum import Enum

import pygame

from src.config import CONFIG


class ButtonState(Enum):
    NORMAL = 0
    CLICKED = 1
    HOVERED = 2
    RELEASED = 3


class Button:

    def __init__(self, x_pos: int,
                y_pos: int,
                label: str,
                width: int=None,
                height: int=None,
                font_color: tuple=(22, 22, 22,),
                outline_color: tuple=(200, 50, 40),
                outline_thickness: int=8,
                font_family: pygame.font.Font=None):

        self.state = ButtonState.NORMAL
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.label = label
        self.width = width if width is not None else len(label) * CONFIG.CHARACTER_SIZE + 2 * CONFIG.CHARACTER_SIZE
        self.height = height if height is not None else len(label.splitlines()) * 2 * CONFIG.CHARACTER_SIZE
        self.outline_thickness = outline_thickness

        self.outline_color = outline_color
        self.clicked_outline_color = (250, 220, 110,)

        self.font_color = font_color
        self.hover_font_color = font_color
        self.label_sprite = None
        self.hover_label_sprite = None
        self.set_label(label, font_family)
     
    def set_label(self, label: str, font_family: pygame.font.Font=None):
        self.label_sprite = font_family.render(label, 1, self.font_color) \
            if font_family is not None else CONFIG.gui_font.render(label, 1, self.font_color)
        self.hover_label_sprite = font_family.render(label, 1, self.hover_font_color) \
            if font_family is not None else CONFIG.gui_font.render(label, 1, self.hover_font_color)

    def display(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] > self.x_pos and mouse_pos[1] > self.y_pos and mouse_pos[0] < self.x_pos + self.width and mouse_pos[1] < self.y_pos + self.height:
            if pygame.mouse.get_pressed()[0]:
                self.state = ButtonState.CLICKED
            elif self.state == ButtonState.CLICKED:
                self.state = ButtonState.RELEASED
            else:
                self.state = ButtonState.HOVERED
        else:
            self.state = ButtonState.NORMAL

        # Show the body the outline and the label of the button
        # Change button according to state
        if self.state == ButtonState.HOVERED:
            pygame.draw.rect(screen, self.outline_color, (self.x_pos, self.y_pos, self.width, self.height))
            screen.blit(self.hover_label_sprite, (self.x_pos + self.width // 4, self.y_pos + self.height // 4))
        elif self.state == ButtonState.CLICKED or self.state == ButtonState.RELEASED:
            pygame.draw.rect(screen, self.clicked_outline_color, (self.x_pos, self.y_pos, self.width, self.height))
            screen.blit(self.label_sprite, (self.x_pos + self.width // 4, self.y_pos + self.height // 4))
        else:
            pygame.draw.rect(screen, self.outline_color, (self.x_pos, self.y_pos, self.width, self.height))
            pygame.draw.rect(screen, CONFIG.BG_COLOR, (self.x_pos + self.outline_thickness // 2,
                                        self.y_pos + self.outline_thickness // 2,
                                        self.width - self.outline_thickness,
                                        self.height - self.outline_thickness))
            screen.blit(self.label_sprite, (self.x_pos + self.width // 4, self.y_pos + self.height // 4))
