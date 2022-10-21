from game.Game import Game
import json, pygame
from config import *

fileSave = open("./filesave.json")
saveData = json.load(fileSave)
fileSave.close()

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGTH))
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)

gameRuning = True

if gameRuning:
    game = Game(screen, saveData)
    game.play()
