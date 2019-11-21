"""
Abstract class for describing levels.
"""
import pygame

from src.config import CONFIG
from src.gfx.map_elements.active_tiles import ActiveTiles


class Level:
    player = None  # Player object
    map = None  # Map object
    last_objective_id: int = 0  # This ID must be incremented after creating a new objective
    objectives: dict = {
        # The key is the ID of the objective
        # the value is in the format of:
        #
        # pos: coordinate list of [from x, to x from y, to y]
        #
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
        # they must have a function of:
        # display(self, screen: pygame.Surface, player: Player)
    ]
    can_show_objectives: bool = True
    objective_window: pygame.Surface = None
    objective_title: pygame.Surface = CONFIG.objective_font.render('OBJECTIVES', 1, (128, 255, 0,))

    def get_entity(self, entity_id: int):
        if entity_id == 0:
            return self.player

        for entity in self.entities:
            if entity.entity_id == entity_id:
                return entity
        return None

    def add_objective(self, desc: str, pos: tuple, font_color: tuple=(250, 252, 255,), is_active: bool=True):
        self.objectives[self.last_objective_id] = {
            'desc': CONFIG.objective_font.render(desc, 1, font_color),
            'pos': pos,
            'is_active': is_active
        }
        self.last_objective_id += 1
        self.drawable_elements.append(ActiveTiles(self.last_objective_id - 1, *pos))

    def remove_objective(self, searched_objective_id: int):
        for objective_id, objective in self.objectives.items():
            if objective_id == searched_objective_id:
                objective['is_active'] = False
                break

        del_index = -1
        for i, drawable_element in enumerate(self.drawable_elements):
            if drawable_element.objective_id == searched_objective_id:
                del_index = i
                break

        if del_index != -1:
            del self.drawable_elements[del_index]

    def display(self, screen: pygame.Surface):
        self.map.display(screen, self.player, self.entities)
        self.player.display(screen, self.map)

        for talk_box in self.talk_boxes:
            if not talk_box.is_clicked:
                talk_box.display(screen, self.get_entity(talk_box.entity_id))

        # Draw graphical elements
        for drawable_element in self.drawable_elements:
            drawable_element.display(screen, self.player)

        # Draw entities
        for entity in self.entities:
            entity.camera_x = self.player.camera_x
            entity.camera_y = self.player.camera_y
            entity.display(screen, self.map)

        if self.objectives and self.can_show_objectives:

            # Display the objectives "window"
            if self.objective_window is None:
                max_obj_width = max([o['desc'].get_size()[0] for o in self.objectives.values()])
                self.objective_window = pygame.Surface((max_obj_width + 15, 24 + 1.5 * CONFIG.OBJECTIVE_FONT_SIZE * len(self.objectives.values())))
                self.objective_window.set_alpha(120)
                self.objective_window.fill((7, 7, 7))

            screen.blit(self.objective_window, (0, 0,))
            screen.blit(self.objective_title, (5, 5,))
            there_is_no_active_objective = True

            # Draw objectives
            for i, (objective_id, objective,) in enumerate(self.objectives.items()):
                if not objective['is_active']:
                    continue
                
                there_is_no_active_objective = False
                screen.blit(objective['desc'], (7, i * 23 + 25,))

            if there_is_no_active_objective:
                # TODO: Step one level up
                pass

        self.after_display(screen)

    def after_display(self, screen: pygame.Surface):
        pass
