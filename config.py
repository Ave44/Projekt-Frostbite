import os.path

import pygame

WINDOW_WIDTH = 1280  # 1920
WINDOW_HEIGHT = 720  # 1080
FPS = 60
TILE_SIZE = 64
CAPTION = 'Project Frostbite'
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ICON = pygame.image.load(f"{ROOT_PATH}/graphics/icon.png")

# SLOTS
SLOT_SIZE = pygame.image.load(f"{ROOT_PATH}/graphics/ui/slot.png").get_size()[0]
SLOT_GAP = 6

# UI
BG_COLOR = (50, 50, 50)
BORDER_COLOR = (255, 255, 255)
BORDER_SIZE = 3
HEALTHBAR_MAIN = (214, 30, 17)
HEALTHBAR_INCREASE = (82, 255, 20)
HEALTHBAR_DECREASE = (240, 212, 29)

# COLORS
BASE_BUTTON_COLOR = "#d7fcd4"
WHITE = "White"
FONT_MENU_COLOR = "#b68f40"

# MUSIC
MAIN_THEME_VOLUME = 0.5
HAPPY_THEME = 'music/custom/happy-theme.mp3'
MENU_THEME = 'music/custom/menu_theme.mp3'

# FONTS
BUTTON_FONT = "graphics/fonts/font.ttf"
