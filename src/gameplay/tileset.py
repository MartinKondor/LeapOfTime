"""
Tileset class.
"""
import pygame


class Tileset:

    def __init__(self, file_name, tile_size=(16, 16,)):
        self.tiles = []
        self.tile_size = tile_size

        image = pygame.image.load(file_name)
        img_size = image.get_size()

        # Load the tileset matrix
        for j in range(img_size[1] // tile_size[1]):
            for i in range(img_size[0] // tile_size[0]):
                image.set_clip(pygame.Rect(i * tile_size[0], j * tile_size[1], tile_size[0], tile_size[1]))
                self.tiles.append(image.subsurface(image.get_clip()))
