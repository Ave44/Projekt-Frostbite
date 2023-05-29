import os.path
from pygame import Color
from pygame.image import load

TILE_SIZE = 128
CAPTION = 'Project Frostbite'
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ICON = load(f"{ROOT_PATH}/graphics/icon.png")
BIOMES_ID = {0: 'sea', 1: 'beach', 2: 'medow', 3: 'forest', 4: 'rocky', 5: 'swamp'}

# UI
BG_COLOR = Color(50, 50, 50)
BORDER_COLOR = Color(255, 255, 255)
BORDER_SIZE = 3
HEALTHBAR_MAIN = Color(214, 30, 17)
HEALTHBAR_INCREASE = Color(82, 255, 20)
HEALTHBAR_DECREASE = Color(240, 212, 29)

HUNGERBAR_MAIN = Color(224, 150, 20)
HUNGERBAR_INCREASE = Color(170, 230, 60)
HUNGERBAR_DECREASE = Color(179, 78, 32)

# SLOTS
SLOT_SIZE = load(f"{ROOT_PATH}/graphics/ui/slot.png").get_size()[0]
SLOT_GAP = 6

# COLORS
BASE_BUTTON_COLOR = "#d7fcd4"
WHITE = "White"
FONT_COLOR = Color(255, 255, 255)
FONT_MENU_COLOR = "#b68f40"
DELETE_SAVEFILE_COLOR = Color(179, 12, 12)

CLOCK_OUTLINE = Color(0, 0, 0)
CLOCK_OUTLINE_SHADOW = Color(0, 0, 0, 64)
SHADOW = Color(0, 0, 0, 160)
COLLIDER_COLOR = Color(255,0,0)

AUTUMN_DAWN_COLOR = Color(205, 131, 122)
AUTUMN_DAY_COLOR = Color(254, 212, 86)
AUTUMN_DUSK_COLOR = Color(165, 91, 82)
AUTUMN_NIGHT_COLOR = Color(46, 54, 87)
AUTUMN_COLORS = [AUTUMN_DAWN_COLOR, AUTUMN_DAY_COLOR, AUTUMN_DUSK_COLOR, AUTUMN_NIGHT_COLOR]

WINTER_DAWN_COLOR = Color(212, 170, 165)
WINTER_DAY_COLOR = Color(250, 226, 155)
WINTER_DUSK_COLOR = Color(125, 93, 89)
WINTER_NIGHT_COLOR = Color(16, 28, 74)
WINTER_COLORS = [WINTER_DAWN_COLOR, WINTER_DAY_COLOR, WINTER_DUSK_COLOR, WINTER_NIGHT_COLOR]

SPRING_DAWN_COLOR = Color(157, 205, 122)
SPRING_DAY_COLOR = Color(175, 252, 81)
SPRING_DUSK_COLOR = Color(139, 181, 166)
SPRING_NIGHT_COLOR = Color(21, 71, 87)
SPRING_COLORS = [SPRING_DAWN_COLOR, SPRING_DAY_COLOR, SPRING_DUSK_COLOR, SPRING_NIGHT_COLOR]

SUMMER_DAWN_COLOR = Color(252, 207, 116)
SUMMER_DAY_COLOR = Color(255, 151, 15)
SUMMER_DUSK_COLOR = Color(77, 19, 30)
SUMMER_NIGHT_COLOR = Color(63, 20, 82)
SUMMER_COLORS = [SUMMER_DAWN_COLOR, SUMMER_DAY_COLOR, SUMMER_DUSK_COLOR, SUMMER_NIGHT_COLOR]

# MUSIC
HAPPY_THEME = 'music/custom/happy-theme.mp3'
MENU_THEME = 'music/custom/menu_theme.mp3'

# FONTS
FONT_SIZE_TINY = 16
FONT_SIZE = 24
FONT_SIZE_BIG = 50
FONT_SIZE_HUGE = 100
NORMAL_FONT = "graphics/fonts/RobotoMono-Regular.ttf"
PIXEL_FONT = "graphics/fonts/pixel-font.ttf"

# DAY CYCLE
DAY_LENGTH_MS = 2 * 64 * 1000
NUMBER_OF_DAY_SEGMENTS = 24
