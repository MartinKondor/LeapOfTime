"""
1 level.
"""
from src.config import CONFIG
from src.gameplay.levels.level import Level
from src.gfx.map import Map
from src.gfx.map_elements.talk_box import TalkBox
from src.gameplay.entities.player import Player
from src.gameplay.entities.evil_lord import EvilLord


class Level1(Level):
    
    def __init__(self):
        self.map = Map(CONFIG.BASE_FOLDER + 'maps/1.map')
        self.player = Player(0, CONFIG.BASE_FOLDER + 'gfx/player/player.gif')
        self.game_time = '2019-12-01'
        self.player.max_speed = 4
        self.player.set_pos(300, 50)
