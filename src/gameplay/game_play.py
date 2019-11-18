"""
GamePlay class for managing the gameplay.
"""
import time

import pygame

from src.config import CONFIG
from src.gfx.map import Map
from src.gfx.map_elements.talk_box import TalkBox
from src.gameplay.entities.player import Player
from src.gameplay.entities.evil_lord import EvilLord


class GamePlay:

    def __init__(self):
        self.map = Map()  # Loads the current level
        self.player = Player(0, CONFIG.BASE_FOLDER + 'gfx/player/player.gif')
        
        # The next entity's id.
        # Increased after an entity is created,
        # thus each new entity will get a new id
        self.last_entity_id = 0
        self.talk_boxes = [
            # Stores the talk boxes
        ]
        self.entities = [
            # Entites that must be drawn
        ]
        self.drawable_elements = [
            # Elements that must be drawn
        ]

        if CONFIG.CURRENT_LEVEL == '0':
            self.player.max_speed = 3
            self.player.set_pos(1347, 3857)
        else:
            # Set player to the center of the map
            self.player.set_pos(self.map.layer_size[0] / 2 - self.player.body.width / 4, self.map.layer_size[1] / 2 - self.player.body.height / 2)

        # Level related
        self.blocked_scenes = []
        self.current_scene = 0
        self.current_scene_subscene = 0
        self.current_scene_subscene_timer = time.time()
        self.current_scene_subscene_delay = 0

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
        self.run_level(CONFIG.CURRENT_LEVEL, screen)

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

    def run_level(self, level: str, screen: pygame.Surface):
        if level == '0':
            if self.current_scene not in self.blocked_scenes and self.current_scene != 1 and \
                    self.player.y_pos >= 3744.5:
                self.current_scene = 1
                self.talk_boxes = []
                self.talk_boxes.append(TalkBox(0, 'I need to go home ...'))
            elif self.current_scene not in self.blocked_scenes and self.current_scene != 2 and \
                    self.player.y_pos < 3744.5 and self.player.y_pos >= 3306.5:
                self.current_scene = 2
                self.talk_boxes = []
                self.talk_boxes.append(TalkBox(0, 'I feel dizzy ...'))
                self.player.max_speed = 2
            elif self.current_scene not in self.blocked_scenes and self.current_scene != 3 and \
                    self.player.y_pos <= 3443:
                self.current_scene = 3
                self.blocked_scenes.append(3)
                self.talk_boxes = []

            # Run scene with the evil person
            if self.current_scene == 3:
                self.player.max_speed = 0

                if self.current_scene_subscene == 0:
                    self.current_scene_subscene += 1
                    
                    self.last_entity_id += 1
                    self.entities.append(EvilLord(self.last_entity_id, CONFIG.BASE_FOLDER + 'gfx/evil_lord/evil_lord.gif'))
                    self.entities[-1].set_pos(self.player.x_pos, self.player.y_pos - 75)

                    self.talk_boxes.append(TalkBox(0, 'What is this?\nWho are you?'))
                    
                    self.current_scene_subscene_delay = 3
                    self.current_scene_subscene_timer = time.time()
                elif self.current_scene_subscene == 1 and time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
                    self.current_scene_subscene += 1
                    self.talk_boxes = []
                    self.talk_boxes.append(TalkBox(self.last_entity_id, 'Second'))
                    self.current_scene_subscene_delay = 4
                    self.current_scene_subscene_timer = time.time()
