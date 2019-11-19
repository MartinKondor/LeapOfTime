"""
Map class for playable and useable maps.
"""
import os

import pygame

from src.config import CONFIG
from src.gfx.tileset import Tileset
from src.gfx.map_layer import MapLayer

import lib.PAdLib.occluder as occluder
import lib.PAdLib.shadow as shadow


class Map:

    def __init__(self, file_name):
        self.tileset = None
        self.layers = []
        self.layer_size = (0, 0,)

        # Load the map for the correct level
        map_file = open(file_name)
        layer_will_be_solid = False
        in_layer = False

        for line in map_file.read().splitlines():
            if not line:
                continue

            for ch in line + '\n':
                if ch == '#':  # Ignore comments
                    break
                if (not ch or ch.isspace()) and ch != '\n':  # Ignore whitespace
                    continue
                if ch == '{':
                    in_layer = True
                    self.layers.append([])
                    continue
                if ch == '}':
                    self.layers[-1] = MapLayer(self.layers[-1], is_solid=layer_will_be_solid)
                    in_layer = False
                    layer_will_be_solid = False
                    continue

                if in_layer and not ch.isspace():
                    self.layers[-1].append([int(l.strip()) - 1 for l in line.strip().split(',') if l.strip()])  # Parse line
                    break
                elif ch == '*':
                    layer_will_be_solid = True
                    continue
                elif ch == '=':
                    key, value = self.parse_key_value(line)  # Set the given key
                    if key == 'tileset':  # Load the tileset
                        self.tileset = Tileset(CONFIG.BASE_FOLDER + 'tilesets/' + value)
                    break

        map_file.close()
        
        self.layers = self.layers[::-1]
        self.layer_size = (
            self.tileset.tile_size[0] * max([len(layer[0]) for layer in self.layers]),
            self.tileset.tile_size[1] * max([len(layer) for layer in self.layers])
        )

    def parse_key_value(self, line: str):
        key, value = line.split('=')
        key = key.strip()

        if '"' in value:
            value = value.strip().split('"')[1]
        else:
            value = value.strip()
        
        return key, value

    def display(self, screen: pygame.Surface, player, entities):
        """
        Draw the tiles what the user can see.
        """

        """
        shad = shadow.Shadow()
        occluders = []
        """

        for layer in self.layers:
            start_x = player.camera_x / self.tileset.tile_size[0] - 1
            start_y = player.camera_y / self.tileset.tile_size[1] - 1
            end_x = (CONFIG.WINDOW_WIDTH + player.camera_x) / self.tileset.tile_size[0]
            end_y = (CONFIG.WINDOW_HEIGHT + player.camera_y) / self.tileset.tile_size[1]

            if start_x < 0:
                start_x = 0
            if start_y < 0:
                start_y = 0

            for y, tiles in enumerate(layer):
                if y < start_y:
                    continue
                elif y > end_y:
                    break

                for x, tile in enumerate(tiles):
                    if tile == -1 or x < start_x:
                        continue
                    elif x > end_x:
                        break

                    """
                    if layer.is_solid:
                        xp = x * self.tileset.tile_size[0] - player.camera_x
                        yp = y * self.tileset.tile_size[1] - player.camera_y
                        occluders.append(
                            occluder.Occluder([[xp, yp], [xp + self.tileset.tile_size[0], yp], [xp + self.tileset.tile_size[0], yp + self.tileset.tile_size[1]], [xp, yp + self.tileset.tile_size[1]]])
                        )
                    """

                    screen.blit(self.tileset.tiles[tile], (x * self.tileset.tile_size[0] - player.camera_x, y * self.tileset.tile_size[1] - player.camera_y,))

        """
        surf_lighting = pygame.Surface(screen.get_size())
        surf_falloff = pygame.image.load(CONFIG.BASE_FOLDER + '../lib/PAdLib/examples/light_falloff100.png').convert()

        shad.set_occluders(occluders)
        shad.set_radius(100.0)
        mask, draw_pos = shad.get_mask_and_position(False)
        mask.blit(surf_falloff, (0, 0), special_flags=pygame.locals.BLEND_MULT)
        
        draw_pos = list(draw_pos)
        draw_pos[0] = CONFIG.WINDOW_WIDTH / 2 - 50
        draw_pos[1] = CONFIG.WINDOW_HEIGHT / 2 - 50
        draw_pos = tuple(draw_pos)

        surf_lighting.fill((77, 77, 77))
        surf_lighting.blit(mask, draw_pos, special_flags=pygame.locals.BLEND_MAX)
        screen.blit(surf_lighting, (0, 0,), special_flags=pygame.locals.BLEND_MULT)

        # for occ in occluders:
        #     pygame.draw.lines(screen, (255, 255, 255), True, occ.points)
        """
