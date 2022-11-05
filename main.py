from game.Game import Game
import json, pygame
from config import *

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

# Game view
gameRuning = True

if gameRuning:
    game = Game(screen, saveData)
    game.play()
