"""
Map class for playable and useable maps.
"""
from src.config import CONFIG


class Map:

    def __init__(self):
        self.tileset_file_name = ''

        # Load the map for the correct level
        map_file = open(CONFIG.BASE_FOLDER + 'maps/' + CONFIG.CURRENT_LEVEL + '.map')
        current_token = ''
        layers = []
        in_layer = False

        for line in map_file.read().splitlines():
            for ch in line:

                # Ignore comments
                if ch == '#':
                    break

                # Ignore whitespace
                if not line or line.isspace():
                    continue

                if ch == '=':
                    current_token = ''
                    key, value = self.parse_key_value(line)

                    # Set the given key
                    if key == 'tileset':
                        self.tileset_file_name = value

                    break

                if ch == '{':
                    in_layer = True
                    layers.append([])
                    continue
                elif ch == '}':
                    in_layer = False
                    continue

                if ch == ',':
                    print(current_token)
                    current_token = ''

                current_token += ch

        map_file.close()

        print(layers[-1])

    def parse_key_value(self, line):
        key, value = line.split('=')
        key = key.strip()
        value = value.strip().split('"')[1]
        return key, value

    def display(self, screen):
        pass
