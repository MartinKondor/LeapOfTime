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
        self.can_show_hud = True
        self.game_time = '2019-12-01'  # The time in which the player plays

        # Load the HUD
        self.hud_elements = []
        self.hud_width = 64
        self.hud_height = 32
        self.hud_game_time_sprite = CONFIG.hud_font.render(self.game_time, 1, (50, 53, 63,))
        hud_img = pygame.image.load(CONFIG.BASE_FOLDER + 'gfx/hud/hud.png').convert()
        # hud_img.set_alpha(220)
        hud_img.set_colorkey((0, 255, 0,))

        for x in range(3):
            hud_img.set_clip(pygame.Rect(x * self.hud_width, 0, self.hud_width, self.hud_height))
            img = hud_img.subsurface(hud_img.get_clip())
            self.hud_elements.append(pygame.transform.scale(img, (128, 64,)))

        # Scretch the center to fill any screen width
        self.hud_width = 128
        self.hud_height = 64
        self.hud_elements[1] = pygame.transform.scale(self.hud_elements[1], (CONFIG.WINDOW_WIDTH - 2 * self.hud_width, self.hud_height,))

        # Intro variables
        self.intro_timer = time.time()
        self.intro_time = 2
        self.intro_shown = CONFIG.DEBUG  # Do not show intro on debug mode

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

        # Setup the current level
        if CONFIG.CURRENT_LEVEL == '0':
            self.player.max_speed = 4
            self.player.set_pos(1347, 3857)
        if CONFIG.CURRENT_LEVEL == '1':
            self.player.max_speed = 4
            # self.player.set_pos(1347, 3857)
        else:
            # Set player to the center of the map
            self.player.set_pos(self.map.layer_size[0] / 2 - self.player.body.width / 4, self.map.layer_size[1] / 2 - self.player.body.height / 2)

    def get_entity(self, entity_id: int):
        if entity_id == 0:
            return self.player

        for entity in self.entities:
            if entity.entity_id == entity_id:
                return entity
        return None

    def display(self, screen: pygame.Surface):
        if not self.intro_shown:
            screen.fill(CONFIG.BG_COLOR)

            level_str = 'LEVEL ' + str(int(CONFIG.CURRENT_LEVEL) + 1)
            screen.blit(CONFIG.readable_font.render(level_str, 1, (240, 249, 255,)),
                        (CONFIG.WINDOW_WIDTH / 2 - (len(level_str) * CONFIG.CHARACTER_SIZE / 4), CONFIG.WINDOW_HEIGHT / 2,))

            screen.blit(CONFIG.readable_font.render(self.game_time, 1, (240, 249, 255,)),
                        (CONFIG.WINDOW_WIDTH / 2 - (len(level_str) * CONFIG.CHARACTER_SIZE / 4), CONFIG.WINDOW_HEIGHT / 2 + 2 * CONFIG.CHARACTER_SIZE,))

            if time.time() - self.intro_timer >= self.intro_time:
                self.intro_shown = True
        else:
            self.map.display(screen, self.player, self.entities)
            self.player.display(screen, self.map)
            
            if CONFIG.CURRENT_LEVEL == '0':
                pass

            # Display HUD
            if self.can_show_hud:
                self.show_hud(screen)

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

    def show_hud(self, screen: pygame.Surface):
        
        # Draw HUD
        screen.blit(self.hud_elements[0], (0, CONFIG.WINDOW_HEIGHT - self.hud_height,))
        screen.blit(self.hud_elements[1], (self.hud_width, CONFIG.WINDOW_HEIGHT - self.hud_height,))
        screen.blit(self.hud_elements[2], (CONFIG.WINDOW_WIDTH - self.hud_width, CONFIG.WINDOW_HEIGHT - self.hud_height,))
        
        screen.blit(self.hud_game_time_sprite, (CONFIG.WINDOW_WIDTH - len(self.game_time) * 13 + 32, CONFIG.WINDOW_HEIGHT - 32,))
