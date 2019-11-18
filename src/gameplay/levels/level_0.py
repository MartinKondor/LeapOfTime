"""
Level 0.
"""
import time

import pygame

from src.gfx.map_elements.talk_box import TalkBox
from src.gameplay.entities.evil_lord import EvilLord
from src.config import CONFIG


def level_0(self, screen: pygame.Surface):
    """
    :param self: GamePlay class
    :returns bool: True if the level ended False if it still moves
    """

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
            self.player.y_pos <= 3443 and self.player.y_pos > 2896:
        self.current_scene = 3
        self.blocked_scenes.append(3)
        self.talk_boxes = []
    elif self.current_scene != 4 and self.player.y_pos <= 2896 and self.player.y_pos > 1221:
        self.current_scene = 4
        self.talk_boxes.append(TalkBox(0, 'Can\'t wait to get home.'))
        self.player.max_speed += 1

    # Run scene with the evil person
    if self.current_scene == 3 and not CONFIG.DEBUG:
        if self.current_scene_subscene == 1:
            self.player.max_speed = 0
            self.current_scene_subscene += 1
            self.last_entity_id += 1
            self.entities.append(EvilLord(self.last_entity_id, CONFIG.BASE_FOLDER + 'gfx/evil_lord/evil_lord.gif'))
            self.entities[-1].set_pos(self.player.x_pos, self.player.y_pos - 75)
            self.talk_boxes.append(TalkBox(0, 'What is this?\nWho are you?'))
            self.current_scene_subscene_delay = 2
            self.current_scene_subscene_timer = time.time()
        elif self.current_scene_subscene == 2 and \
                time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
            self.current_scene_subscene += 1
            self.talk_boxes = []
            self.talk_boxes.append(TalkBox(self.last_entity_id, 'I am the Lord.'))
            self.current_scene_subscene_delay = 2
            self.current_scene_subscene_timer = time.time()
        elif self.current_scene_subscene == 3 and \
                time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
            self.current_scene_subscene += 1
            self.talk_boxes = []
            self.talk_boxes.append(TalkBox(self.last_entity_id, 'I came here because\nI need your power.'))
            self.current_scene_subscene_delay = 3
            self.current_scene_subscene_timer = time.time()
        elif self.current_scene_subscene == 4 and \
                time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
            self.current_scene_subscene += 1
            self.talk_boxes = []
            self.talk_boxes.append(TalkBox(self.last_entity_id, 'If you help\nI will give the most\nprecious thing you need ...'))
            self.current_scene_subscene_delay = 4
            self.current_scene_subscene_timer = time.time()
        elif self.current_scene_subscene == 5 and \
                time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
            self.current_scene_subscene += 1
            self.talk_boxes.append(TalkBox(0, 'What?!'))
            self.current_scene_subscene_delay = 2
            self.current_scene_subscene_timer = time.time()
        elif self.current_scene_subscene == 6 and \
                time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
            self.current_scene_subscene += 1
            self.talk_boxes = []
            self.talk_boxes.append(TalkBox(self.last_entity_id, 'Money.'))
            self.current_scene_subscene_delay = 2
            self.current_scene_subscene_timer = time.time()
        elif self.current_scene_subscene == 7 and \
                time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
            self.current_scene_subscene += 1
            self.talk_boxes.append(TalkBox(0, 'Money ...'))
            self.current_scene_subscene_delay = 2
            self.current_scene_subscene_timer = time.time()
            self.show_hud = True
        elif self.current_scene_subscene == 8 and \
                time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
            self.current_scene_subscene += 1
            self.talk_boxes = []
            self.talk_boxes.append(TalkBox(self.last_entity_id, 'Go home.\nYour first quest\nwill begin there.'))
            self.current_scene_subscene_delay = 3
            self.current_scene_subscene_timer = time.time()
        elif self.current_scene_subscene == 9 and \
                time.time() - self.current_scene_subscene_timer >= self.current_scene_subscene_delay:
            self.talk_boxes = []
            self.entities = []
            self.current_scene_subscene = 0
            self.player.max_speed = 4

        # Arrived home
        return self.player.y_pos <= 1280 and self.player.x_pos <= 1156 and self.player.x_pos >= 1042
