import pygame
from pygame import mixer

from constants import CAPTION, ICON
from Config import Config

from menu.MainMenu import MainMenu

# Program initialization
pygame.init()
config = Config()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)

# Initialize music
mixer.init()
mixer.music.set_volume(config.MUSIC_VOLUME)

# Game view
gameRunning = True

if gameRunning:
    menu = MainMenu(screen, config)
    menu.mainMenu()
