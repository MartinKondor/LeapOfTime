"""
Player class for playable charachers.
"""
import pygame

from src.config import CONFIG


class Player:
    
    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0
        self.x_pos = 0
        self.y_pos = 0
        self.x_speed = 0
        self.y_speed = 0
        self.max_speed = 12

    def display(self, screen):
        pressed_keys = pygame.key.get_pressed()

        # Move on keypress
        if pressed_keys[CONFIG.KEY_RIGHT]:
            self.x_speed += CONFIG.BASE_SPEED
        elif pressed_keys[CONFIG.KEY_LEFT]:
            self.x_speed -= CONFIG.BASE_SPEED
        else:
            self.x_speed = 0

        if pressed_keys[CONFIG.KEY_DOWN]:
            self.y_speed += CONFIG.BASE_SPEED
        elif pressed_keys[CONFIG.KEY_UP]:
            self.y_speed -= CONFIG.BASE_SPEED
        else:
            self.y_speed = 0

        # Check max speed
        if self.x_speed > self.max_speed:
            self.x_speed = self.max_speed
        if self.y_speed < -self.max_speed:
            self.y_speed = -self.max_speed

        # Apply changes
        self.camera_x = self.x_pos - CONFIG.WINDOW_WIDTH / 2
        self.camera_y = self.y_pos - CONFIG.WINDOW_HEIGHT / 2

        # Do not let the user see the corner of the map
        if self.camera_x < 0:
            self.camera_x = 0
        else:
            self.x_pos += self.x_speed

        if self.camera_y < 0:
            self.camera_y = 0
        else:
            self.y_pos += self.y_speed

        print((self.camera_x, self.camera_y), (self.x_pos, self.y_pos), (self.x_speed, self.y_speed))
