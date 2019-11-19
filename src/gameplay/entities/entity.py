"""
Common class for game entites.
"""

class Entity:
    entity_id: int = None
    x_pos: float = 0
    y_pos: float = 0
    x_speed: float = 0
    y_speed: float = 0
    camera_x: float = 0
    camera_y: float = 0
    max_speed: float = 7
    animation_file_name: str = None
    body = None  # Animation class
    direction = None  # AnimationDirection class

    def collision_detection(self, map):
        """
        Checks for collision detection and if there is a collision
        stops the entity from moving.
        """
        for layer in map.layers:
            if not layer.is_solid:
                continue

            # Only check the really close tiles
            start_x = self.x_pos / map.tileset.tile_size[0] - 2
            start_y = self.y_pos / map.tileset.tile_size[1] - 2
            end_x = self.x_pos / map.tileset.tile_size[0] + 3
            end_y = self.y_pos / map.tileset.tile_size[1] + 3

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

                    # Get the position of the tiles
                    x_pos = x * map.tileset.tile_size[0] - self.camera_x
                    y_pos = y * map.tileset.tile_size[1] - self.camera_y

                    # Check for collision
                    if self.x_speed + self.x_pos - self.camera_x - self.body.width / 4 > x_pos - 2 * map.tileset.tile_size[0] and \
                        self.x_speed + self.x_pos - self.camera_x + self.body.width / 4 < x_pos + map.tileset.tile_size[0] and \
                        self.y_speed + self.y_pos - self.camera_y + self.body.height / 2 < y_pos + map.tileset.tile_size[1] and \
                        self.y_speed + self.y_pos - self.camera_y > y_pos - 2 * map.tileset.tile_size[1]:
                            
                            # Stop the entity from moving
                            if self.x_speed != 0:
                                self.x_speed = 0
                            
                            if self.y_speed != 0:
                                self.y_speed = 0
