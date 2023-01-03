import json

from pygame import mixer

from config import *
from game.Game import Game

# loading savefile
# (Later will be replaced with "load all savefile names", then only selected favefile will be loaded)
fileSave = open("./filesave.json")
saveData = json.load(fileSave)
fileSave.close()

# Program initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)

# Initialize music
mixer.init()
mixer.music.load('music/custom/main_theme.mp3')
mixer.music.play(-1)
mixer.music.set_volume(MAIN_THEME_VOLUME)
# Game view
gameRunning = True

if gameRunning:
    game = Game(screen, saveData)
    game.main_menu()
