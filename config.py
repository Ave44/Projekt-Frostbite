import os.path
import pygame


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TILE_SIZE = 64
CAPTION = 'Project Frostbite'
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ICON = pygame.image.load(f"{ROOT_PATH}/graphics/icon.png")
SLOTSIZE = pygame.image.load(f"{ROOT_PATH}/graphics/ui/slot.png").get_size()[0]
SLOTGAP = 6

UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = 'white'
UI_BORDER_SIZE = 3
