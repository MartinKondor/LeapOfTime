"""
Player class for playable charachers.
"""
import pygame

from src.gameplay.entity import Entity
from src.config import CONFIG
from src.gfx.animation import Animation, AnimationDirection


class Player(Entity):
    
    def __init__(self, entity_id: int, animation_file_name: str):
        self.entity_id = entity_id
        self.x_pos = 0
        self.y_pos = 0
        self.x_speed = 0
        self.y_speed = 0
        self.max_speed = 7
        self.animation_file_name = animation_file_name
        self.body = Animation(animation_file_name, (64, 64,))
        self.direction = AnimationDirection.DOWN

        self.camera_x = 0
        self.camera_y = 0

    def set_pos(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.camera_x = x_pos
        self.camera_y = y_pos

    def display(self, screen: pygame.Surface, map):
        pressed_keys = pygame.key.get_pressed()

        # Move on keypress
        if pressed_keys[CONFIG.KEY_RIGHT]:
            self.x_speed += CONFIG.BASE_SPEED
            self.direction = AnimationDirection.RIGHT
        elif pressed_keys[CONFIG.KEY_LEFT]:
            self.x_speed -= CONFIG.BASE_SPEED
            self.direction = AnimationDirection.LEFT
        else:
            self.x_speed = 0

        if pressed_keys[CONFIG.KEY_DOWN]:
            self.y_speed += CONFIG.BASE_SPEED
            self.direction = AnimationDirection.DOWN
        elif pressed_keys[CONFIG.KEY_UP]:
            self.y_speed -= CONFIG.BASE_SPEED
            self.direction = AnimationDirection.UP
        else:
            self.y_speed = 0

        # Check max speed
        if self.x_speed > self.max_speed:
            self.x_speed = self.max_speed
        if self.x_speed < -self.max_speed:
            self.x_speed = -self.max_speed
        if self.y_speed > self.max_speed:
            self.y_speed = self.max_speed
        if self.y_speed < -self.max_speed:
            self.y_speed = -self.max_speed

        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        self.camera_x = self.x_pos - CONFIG.WINDOW_WIDTH / 2
        self.camera_y = self.y_pos - CONFIG.WINDOW_HEIGHT / 2

        # Do not let the user see the corner of the map
        if self.camera_x <= 0:
            self.camera_x = 0
        if self.camera_y <= 0:
            self.camera_y = 0
        if self.camera_x >= map.layer_size[0]:
            self.camera_x = map.layer_size[0]
        if self.camera_y >= map.layer_size[1]:
            self.camera_y = map.layer_size[1]

        # TODO: Do not let the user go out from the map
        if self.x_pos + map.tileset.tile_size[0] < 0:
            self.x_pos = -map.tileset.tile_size[0]
            self.x_speed = 0
        if self.y_pos + map.tileset.tile_size[1] < 0:
            self.y_pos = -map.tileset.tile_size[1]
            self.y_speed = 0
        """
        if self.x_pos - 2 * self.body.width - map.tileset.tile_size[0] > 1.5 * self.camera_x:
            self.x_pos = 1.5 * self.camera_x + (2 * self.body.width - map.tileset.tile_size[0])
            self.x_speed = 0
        if self.y_pos + self.body.height / 2 + map.tileset.tile_size[1] > 1.5 * self.camera_y:
            self.y_pos = 1.5 * self.camera_y - (self.body.height / 2 + map.tileset.tile_size[1])
            self.y_speed = 0
        """

        # print('Camera:', (self.camera_x, self.camera_y), 'Pos:', (self.x_pos, self.y_pos), 'Speed:', (self.x_speed, self.y_speed))

        self.body.display(screen, self)
