"""
Map class for playable and useable maps.
"""
import os

import pygame

from src.config import CONFIG
from src.gameplay.tileset import Tileset


class Map:

    def __init__(self):
        self.layers = []
        self.tileset = None

        # Load the map for the correct level
        map_file = open(CONFIG.BASE_FOLDER + 'maps/' + CONFIG.CURRENT_LEVEL + '.map')
        current_token = ''

        for line in map_file.read().splitlines():
            for ch in line + '\n':

                # Ignore comments
                if ch == '#':
                    break

                # Ignore whitespace
                if (not ch or ch.isspace()) and ch != '\n':
                    continue

                if ch == '=':
                    current_token = ''
                    key, value = self.parse_key_value(line)

                    # Set the given key
                    if key == 'tileset':
                        # Load the tileset
                        self.tileset = Tileset(CONFIG.BASE_FOLDER + 'tilesets/' + value)
                    break

                if ch == '{':
                    self.layers.append([])
                    continue
                elif ch == '}':
                    self.layers[-1] = [[int(num.strip()) for num in line.split(',') if num.strip()] for line in current_token.splitlines() if line]
                    continue

                current_token += ch

        map_file.close()

    def parse_key_value(self, line):
        key, value = line.split('=')
        key = key.strip()
        value = value.strip().split('"')[1]
        return key, value

    def display(self, player, screen):
        for layer in self.layers:
            layer_width = len(layer[0])
            layer_height = len(layer)

            start_x = player.camera_x / 32 - 2
            if start_x < 0:
                start_x = 0
            
            start_y = player.camera_y / 32 - 2
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
                    if tile == 0 or x < start_x:
                        continue
                    elif x > end_x:
                        break

                    screen.blit(self.tileset.tiles[tile], (x * self.tileset.tile_size[0] - player.camera_x, y * self.tileset.tile_size[1] - player.camera_y,))
        
        return
        for layer in self.layers:  # Draw layers
            for row in layer:
                for tile_index in row:
                    screen.blit(self.tileset.tiles[tile_index], (0, 0,))
