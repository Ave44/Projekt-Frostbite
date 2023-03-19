import os.path
import math
import pygame

WINDOW_WIDTH = 1920  # 1280
WINDOW_HEIGHT = 1080  # 720
TILE_SIZE = 128
TILES_ON_SCREEN_WIDTH = math.ceil(WINDOW_WIDTH / TILE_SIZE + 1)
TILES_ON_SCREEN_HEIGHT = math.ceil(WINDOW_HEIGHT / TILE_SIZE + 1)
CAPTION = 'Project Frostbite'
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ICON = pygame.image.load(f"{ROOT_PATH}/graphics/icon.png")
BIOMES_ID = {0: 'sea', 1: 'beach', 2: 'medow', 3: 'forest', 4: 'rocky', 5: 'swamp'}

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
MAIN_THEME_VOLUME = 0#.5
HAPPY_THEME = 'music/custom/happy-theme.mp3'
MENU_THEME = 'music/custom/menu_theme.mp3'

# FONTS
BUTTON_FONT = "graphics/fonts/font.ttf"
