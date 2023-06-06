import pygame
from pygame import mixer
from pygame._sdl2.video import Window

from constants import CAPTION, ICON
from Config import Config

from menu.MenuController import MenuController

# Program initialization
pygame.init()

config = Config()
pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)
config.window = Window.from_display_module()

# Initialize music
mixer.init()
mixer.music.set_volume(config.MUSIC_VOLUME)

# Game view
menuController = MenuController(config)
menuController.menuLoop()
