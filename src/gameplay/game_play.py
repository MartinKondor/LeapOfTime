"""
GamePlay class for managing the gameplay.
"""
import pygame

from src.config import CONFIG
from src.gfx.map import Map
from src.gameplay.player import Player
from src.gfx.map_elements.talk_box import TalkBox


class GamePlay:

    def __init__(self):
        self.map = Map()  # Loads the current level
        self.player = Player(0, CONFIG.BASE_FOLDER + 'gfx/player/player.gif')
        
        # The next entity's id.
        # Increased after an entity is created,
        # thus each new entity will get a new id
        self.last_entity_id = 0
        
        # Set player to the center of the map
        self.player.set_pos(self.map.layer_size[0] / 2 - self.player.body.width / 4, self.map.layer_size[1] / 2 - self.player.body.height / 2)
        
        if CONFIG.CURRENT_LEVEL == '0':
            self.player.max_speed = 3

        self.talk_boxes = [
            # Stores the talk boxes
        ]
        self.entities = [
            # Entites that must be drawn
        ]
        self.drawable_elements = [
            # Elements that must be drawn
        ]  

    def get_entity(self, entity_id: int):
        if entity_id == 0:
            return self.player

        for entity in self.entities:
            if entity.entity_id == entity_id:
                return entity
        return None

    def display(self, screen: pygame.Surface):
        self.map.display(screen, self.player, self.entities)
        self.player.display(screen, self.map)

        if CONFIG.CURRENT_LEVEL == '0':
            pass

        for talk_box in self.talk_boxes:
            talk_box.display(screen, self.get_entity(talk_box.entity_id), self.player)

        # Draw graphical elements
        for drawable_element in self.drawable_elements:
            pass

        # Draw entities
        for entity in self.entities:
            pass
