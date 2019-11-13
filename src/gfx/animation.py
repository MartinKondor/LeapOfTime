"""
Animation for characters and animated elements.
"""
import time

import pygame

from enum import IntEnum


class AnimationDirection(IntEnum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


class Animation:

    def __init__(self, file_name, anim_size=(64, 64,)):
        self.frames = []
        self.max_frame = 2
        self.frame_index = 0
        self.animation_frames_per_second = 4
        self.animation_clock = time.time()

        anim_img = pygame.image.load(file_name)
        anim_img.set_colorkey((0, 255, 0),)

        for j in range(4):
            anim_frames = []

            for i in range(self.max_frame):
                anim_img.set_clip(pygame.Rect(i * anim_size[0], j * anim_size[1], anim_size[0], anim_size[1]))
                img = anim_img.subsurface(anim_img.get_clip())
                anim_frames.append(pygame.transform.scale(img, (42, 42,)))
            
            self.frames.append(anim_frames)

    def display(self, screen, entity):
        screen.blit(self.get_frame(entity.direction), (entity.x_pos - entity.camera_x, entity.y_pos - entity.camera_y,))
        
        if (time.time() - self.animation_clock) >= (1 / self.animation_frames_per_second):
            self.animation_clock = time.time()
            self.frame_index += 1

            if self.frame_index >= self.max_frame:
                self.frame_index = 0

    def get_frame(self, direction):
        return self.frames[direction][self.frame_index]
