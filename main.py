import json

from pygame import mixer

from config import *
from game.Game import Game
from game.Menu import Menu

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
currentMenu = "MAIN"

# Initialize music
mixer.init()
# Game view
gameRunning = True

if gameRunning:
    game = Game(screen, saveData)
    menu = Menu(screen, game.play, currentMenu)
    menu.mainMenu()
