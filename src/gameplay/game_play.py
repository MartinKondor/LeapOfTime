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
from src.gameplay.levels.level_0 import level_0


class GamePlay:

    def __init__(self):
        self.map = Map()  # Loads the current level
        self.player = Player(0, CONFIG.BASE_FOLDER + 'gfx/player/player.gif')
        self.show_hud = True

        # Intro variables
        self.intro_timer = time.time()
        self.intro_time = 2
        self.intro_shown = False if not CONFIG.DEBUG else True

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
            self.show_hud = False
            self.player.max_speed = 3
            self.player.set_pos(1347, 3857)
        else:
            # Set player to the center of the map
            self.player.set_pos(self.map.layer_size[0] / 2 - self.player.body.width / 4, self.map.layer_size[1] / 2 - self.player.body.height / 2)

        # Level related
        self.blocked_scenes = []
        self.current_scene = 0
        self.current_scene_subscene = 1
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
        if not self.intro_shown:
            level_str = 'Level ' + str(int(CONFIG.CURRENT_LEVEL) + 1)
            screen.fill(CONFIG.BG_COLOR)
            screen.blit(CONFIG.readable_font.render(level_str, 1, (240, 249, 255,)),
                        (CONFIG.WINDOW_WIDTH / 2 - (len(level_str) * CONFIG.CHARACTER_SIZE / 4), CONFIG.WINDOW_HEIGHT / 2,))

            if time.time() - self.intro_timer >= self.intro_time:
                self.intro_shown = True
            return

        self.map.display(screen, self.player, self.entities)
        self.player.display(screen, self.map)
        self.run_level(screen)

        # Display HUD
        if self.show_hud:
            pygame.draw.rect(screen, (100, 200, 50,), (3, CONFIG.WINDOW_HEIGHT - 67, 100, 64))

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

    def run_level(self, screen: pygame.Surface):
        if CONFIG.DEBUG:
            print('CONFIG.CURRENT_LEVEL:', CONFIG.CURRENT_LEVEL)
            print('self.current_scene:', self.current_scene)
            print('self.current_scene_subscene:', self.current_scene_subscene)

        if CONFIG.CURRENT_LEVEL == '0':
            if level_0(self, screen):
                CONFIG.CURRENT_LEVEL = '1'
                print('asd')
