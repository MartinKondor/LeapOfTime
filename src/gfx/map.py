"""
Map class for playable and useable maps.
"""
import os

import pygame

from src.config import CONFIG
from src.gfx.tileset import Tileset
from src.gfx.map_layer import MapLayer


class Map:

    def __init__(self):
        self.tileset = None
        self.layers = []
        self.layer_size = (0, 0,)

        # Load the map for the correct level
        map_file = open(CONFIG.BASE_FOLDER + 'maps/' + CONFIG.CURRENT_LEVEL + '.map')
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
            self.tileset.tile_size[0] / 2 * max([len(layer[0]) for layer in self.layers]),
            self.tileset.tile_size[1] / 2 * max([len(layer) for layer in self.layers])
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

        for layer in self.layers:
            layer_width = len(layer[0])
            layer_height = len(layer)

            start_x = player.camera_x / self.tileset.tile_size[0] - 1
            if start_x < 0:
                start_x = 0
            
            start_y = player.camera_y / self.tileset.tile_size[1] - 1
            if start_y < 0:
                start_y = 0

            end_x = (CONFIG.WINDOW_WIDTH + player.camera_x) / self.tileset.tile_size[0]
            if end_x < layer_width - 1:
                end_x = layer_width - 1

            end_y = (CONFIG.WINDOW_HEIGHT + player.camera_y) / self.tileset.tile_size[1]
            if end_y < layer_height - 1:
                end_y = layer_height - 1

            x_pos = None
            y_pos = None

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

                    x_pos = x * self.tileset.tile_size[0] - player.camera_x
                    y_pos = y * self.tileset.tile_size[1] - player.camera_y

                    # TODO: Check intersection with entites if the layer is "solid"
                    if layer.is_solid:
                        for entity in entities + [player]:                            
                            break
                            
                            en_x_pos = entity.x_pos + entity.body.width / 4
                            en_y_pos = entity.y_pos + entity.body.height / 4


                            if en_x_pos < x_pos + 2 * self.tileset.tile_size[0] and en_y_pos < y_pos + 2 * self.tileset.tile_size[1]:
                                print('YES')

                    screen.blit(self.tileset.tiles[tile], (x_pos, y_pos,))
