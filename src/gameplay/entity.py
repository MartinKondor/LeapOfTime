"""
Common class for game entites.
"""

class Entity:
    entity_id: int = None
    x_pos: float = 0
    y_pos: float = 0
    x_speed: float = 0
    y_speed: float = 0
    max_speed: float = 7
    animation_file_name: str = None
    body = None  # Animation class
    direction = None  # AnimationDirection class
