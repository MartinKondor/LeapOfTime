"""
Abstract class for describing levels.
"""
import pygame

from src.config import CONFIG


class Level:
    player = None  # Player object
    map = None  # Map object
    last_objective_id: int = 0  # This ID must be incremented after creating a new objective
    objectives: list = {
        # The key is the ID of the objective
    }
    game_time: str = '2019-12-01'  # What is the time
    last_entity_id: int = 0  # Increased after an entity is created,
    talk_boxes: list = [
        # Stores the talk boxes
    ]
    entities: list = [
        # Entites that must be drawn
        # not including the player
    ]
    drawable_elements: list = [
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

        for talk_box in self.talk_boxes:
            if not talk_box.is_clicked:
                talk_box.display(screen, self.get_entity(talk_box.entity_id))

        # Draw graphical elements
        # for drawable_element in self.drawable_elements:
        #     pass

        # Draw entities
        for entity in self.entities:
            entity.camera_x = self.player.camera_x
            entity.camera_y = self.player.camera_y
            entity.display(screen, self.map)
