import os.path

import pygame

WINDOW_WIDTH = 1280 # 1920
WINDOW_HEIGHT = 720 # 1080
FPS = 60
TILE_SIZE = 64
CAPTION = 'Project Frostbite'
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ICON = pygame.image.load(f"{ROOT_PATH}/graphics/icon.png")
SLOTSIZE = pygame.image.load(f"{ROOT_PATH}/graphics/ui/slot.png").get_size()[0]
SLOTGAP = 6

UI_BG_COLOR = (50,50,50)
UI_BORDER_COLOR = (255,255,255)
UI_BORDER_SIZE = 3
UI_HEALTHBAR_MAIN = (214,30,17)
UI_HEALTHBAR_INCREASE = (82,255,20)
UI_HEALTHBAR_DECREASE = (240,212,29)
MAIN_THEME_VOLUME = 0.5
