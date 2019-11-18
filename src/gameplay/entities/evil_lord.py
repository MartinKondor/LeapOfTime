"""
Player class for playable charachers.
"""
import pygame

from src.gameplay.entities.entity import Entity
from src.gfx.animation import Animation, AnimationDirection


class EvilLord(Entity):
    
    def __init__(self, entity_id: int, animation_file_name: str):
        self.entity_id = entity_id
        self.x_pos = 0
        self.y_pos = 0
        self.x_speed = 0
        self.y_speed = 0
        self.camera_x = 0
        self.camera_y = 0
        self.max_speed = 7
        self.animation_file_name = animation_file_name
        self.body = Animation(animation_file_name, (64, 64,))
        self.direction = AnimationDirection.DOWN

    def set_pos(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def display(self, screen: pygame.Surface, map):

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

        if self.x_pos + map.tileset.tile_size[0] < 0:
            self.x_pos = -map.tileset.tile_size[0]
            self.x_speed = 0
        if self.y_pos + map.tileset.tile_size[1] < 0:
            self.y_pos = -map.tileset.tile_size[1]
            self.y_speed = 0
        if self.x_pos > map.layer_size[0] - self.body.width / 2:
            self.x_pos = map.layer_size[0] - self.body.width / 2
            self.x_speed = 0
        if self.y_pos > map.layer_size[1] - self.body.height / 2:
            self.y_pos = map.layer_size[1] - self.body.height / 2
            self.y_speed = 0

        self.body.display(screen, self)
