import json

from pygame import mixer

from config import *
from game.Game import Game
from game.menu.MainMenu import MainMenu

# loading savefile
# (Later will be replaced with "load all savefile names", then only selected savefile will be loaded)
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
# Game view
gameRunning = True

if gameRunning:
    game = Game(screen, saveData)
    menu = MainMenu(screen, game.play)
    menu.mainMenu()
