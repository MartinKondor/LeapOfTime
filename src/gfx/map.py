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
        current_token = ''
        layer_will_be_solid = False

        for line in map_file.read().splitlines():
            for ch in line + '\n':
                if ch == '#':  # Ignore comments
                    break
                if (not ch or ch.isspace()) and ch != '\n':  # Ignore whitespace
                    continue

                if ch == '=':
                    current_token = ''
                    key, value = self.parse_key_value(line)

                    # Set the given key
                    if key == 'tileset':
                        # Load the tileset
                        self.tileset = Tileset(CONFIG.BASE_FOLDER + 'tilesets/' + value)
                    break

                if ch == '*':
                    layer_will_be_solid = True
                    continue

                # Layers
                if ch == '{':
                    self.layers.append([])
                    continue
                elif ch == '}':
                    self.layers[-1] = MapLayer([[int(num.strip()) - 1 for num in line.split(',') if num.strip()] for line in current_token.splitlines() if line], is_solid=layer_will_be_solid)
                    continue

                current_token += ch

        map_file.close()
        self.layers = self.layers[::-1]
        self.layer_size = (self.tileset.tile_size[0] / 2 * len(self.layers[0][0]), self.tileset.tile_size[1] / 2 * len(self.layers[0]),)

    def parse_key_value(self, line):
        key, value = line.split('=')
        key = key.strip()

        if '"' in value:
            value = value.strip().split('"')[1]
        else:
            value = value.strip()
        
        return key, value

    def display(self, screen, player):
        """
        Draw the tiles what the user can see.
        """

        for layer in self.layers:
            layer_width = len(layer[0])
            layer_height = len(layer)

            start_x = player.camera_x / 32 - 1
            if start_x < 0:
                start_x = 0
            
            start_y = player.camera_y / 32 - 1
            if start_y < 0:
                start_y = 0

            end_x = (CONFIG.WINDOW_WIDTH + player.camera_x) / 32
            if end_x < layer_width - 1:
                end_x = layer_width - 1

            end_y = (CONFIG.WINDOW_HEIGHT + player.camera_y) / 32
            if end_y < layer_height - 1:
                end_y = layer_height - 1

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

                    screen.blit(self.tileset.tiles[tile], (x * self.tileset.tile_size[0] - player.camera_x, y * self.tileset.tile_size[1] - player.camera_y,))
