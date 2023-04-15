import os.path
from pygame import Color
from pygame.image import load

TILE_SIZE = 128
CAPTION = 'Project Frostbite'
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ICON = load(f"{ROOT_PATH}/graphics/icon.png")
BIOMES_ID = {0: 'sea', 1: 'beach', 2: 'medow', 3: 'forest', 4: 'rocky', 5: 'swamp'}

# UI
BG_COLOR = (50, 50, 50)
BORDER_COLOR = (255, 255, 255)
BORDER_SIZE = 3
HEALTHBAR_MAIN = (214, 30, 17)
HEALTHBAR_INCREASE = (82, 255, 20)
HEALTHBAR_DECREASE = (240, 212, 29)

# SLOTS
SLOT_SIZE = load(f"{ROOT_PATH}/graphics/ui/slot.png").get_size()[0]
SLOT_GAP = 6

# COLORS
BASE_BUTTON_COLOR = "#d7fcd4"
WHITE = "White"
FONT_MENU_COLOR = "#b68f40"

CLOCK_OUTLINE = Color(0, 0, 0)
CLOCK_OUTLINE_SHADOW = Color(0, 0, 0, 64)
DAWN_COLOR = Color(205, 131, 122)
DAY_COLOR = Color(254, 212, 86)
EVENING_COLOR = Color(165, 91, 82)
NIGHT_COLOR = Color(46, 54, 87)

# MUSIC
HAPPY_THEME = 'music/custom/happy-theme.mp3'
MENU_THEME = 'music/custom/menu_theme.mp3'

# FONTS
BUTTON_FONT = "graphics/fonts/font.ttf"