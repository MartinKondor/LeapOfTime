"""
Main file for starting the game.
"""
import os
import random as r

import pygame

from src.config import CONFIG
from src.screens.screen import Screens
from src.screens.main_menu import MainMenuScreen
from src.screens.loading import LoadingScreen
from src.screens.game import GameScreen
from src.screens.settings import SettingsScreen


def check_events():
    """
    :returns bool: false if game must be exited
    """
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            return False
    return True


if __name__ == '__main__':
    if not pygame.font:
        print('ERROR: fonts are disabled')
        exit(1)
    if not pygame.mixer:
        print('ERROR: sounds are disabled')
        exit(1)

    # Starting the game
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()
    screen_size = (CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT,)

    if CONFIG.FULLSCREEN:
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(screen_size)

    pygame.display.set_icon(pygame.image.load(CONFIG.BASE_FOLDER + 'images/icon.png'))
    pygame.display.set_caption('Leap Of Time')
    pygame.mouse.set_visible(1)
    game_clock = pygame.time.Clock()

    # Load fonts
    CONFIG.load_fonts()

    # Load songs
    already_played_song_indices = []
    current_song_index = 0
    songs = []

    for song in os.listdir(CONFIG.BASE_FOLDER + 'music'):
        parts = song.split('.')
        if parts[-1] == 'ogg' or parts[-1] == 'mp3':
            songs.append(CONFIG.BASE_FOLDER + 'music/' + song)

    # Play the first song
    pygame.mixer.music.load(songs[current_song_index])
    pygame.mixer.music.set_volume(0.01 * CONFIG.MASTER_VOLUME)
    pygame.mixer.music.play()

    # Loading the current screen
    current_screen_enum = Screens.LOADING
    last_screen_enum = Screens.LOADING
    current_screen = GameScreen()  # LoadingScreen()

    while current_screen_enum != Screens.EXIT and check_events():
        if current_screen_enum == Screens.GAME:
            screen.fill((0, 0, 0))
        else:
            screen.fill(CONFIG.BG_COLOR)

        current_screen_enum = current_screen.display(screen)

        # Change screen if needed
        if current_screen_enum != last_screen_enum:
            if current_screen_enum == Screens.LOADING:
                current_screen = LoadingScreen()
            elif current_screen_enum == Screens.MAIN_MENU:
                current_screen = MainMenuScreen()
            elif current_screen_enum == Screens.SETTINGS:
                current_screen = SettingsScreen()
            elif current_screen_enum == Screens.GAME:
                current_screen = GameScreen()

            last_screen_enum = current_screen_enum

        # Play the songs
        if not pygame.mixer.music.get_busy():
            already_played_song_indices.append(current_song_index)
            current_song_index += 1

            if current_song_index >= len(songs):
                current_song_index = 0
                already_played_song_indices = []
            
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(0.01 * CONFIG.MASTER_VOLUME)
            pygame.mixer.music.load(songs[current_song_index])
            pygame.mixer.music.play()

        game_clock.tick(CONFIG.FPS_LIMIT)
        print('FPS:', int(game_clock.get_fps()))
        pygame.display.update()
        pygame.display.flip()

    pygame.quit()
