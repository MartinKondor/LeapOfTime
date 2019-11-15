"""
TalkBox for showing talking or loud thinking.
"""
import pygame

from src.gameplay.entity import Entity
from src.config import CONFIG


class TalkBox:
    
    def __init__(self, entity_id: int, text: str):
        """
        :param entity_id: int the entity that has this box
        :param text: str of the text to be drawn
        """
        lines = text.split('\n')

        self.entity_id = entity_id
        self.text_sprites = [CONFIG.text_box_font.render(line, 1, (37, 37, 37,)) for line in lines]
        self.padding = 7
        self.width = CONFIG.TALK_BOX_FONT_SIZE * max([len(r) for r in lines]) + self.padding
        self.height = CONFIG.TALK_BOX_FONT_SIZE * len(lines) + self.padding

        # Positions are relative to the entity
        self.x_pos = 42 + self.width / 2
        self.y_pos = -12 * len(lines) + self.height / 2

    def display(self, screen: pygame.Surface, entity: Entity, player):
        x_pos = entity.x_pos - player.camera_x + self.x_pos - self.width / 2
        y_pos = entity.y_pos - player.camera_y + self.y_pos - self.height / 2

        # Hover effect
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] > x_pos and mouse_pos[1] > y_pos and mouse_pos[0] < x_pos + self.width and mouse_pos[1] < y_pos + self.height:
            pygame.draw.rect(screen, (37, 37, 37,), (x_pos - 1, y_pos - 1, self.width + 1, self.height + 1))
        else:
            pygame.draw.rect(screen, (37, 37, 37,), (x_pos + 1, y_pos + 1, self.width + 1, self.height + 1)) 
        
        pygame.draw.rect(screen, (255, 254, 230,), (x_pos, y_pos, self.width, self.height))

        for i, text_sprite in enumerate(self.text_sprites):
            screen.blit(text_sprite, (x_pos + self.padding / 2, i * CONFIG.TALK_BOX_FONT_SIZE + y_pos + self.padding / 2,))
