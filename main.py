from pygame import mixer

from config import *
from menu.MainMenu import MainMenu

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
    menu = MainMenu(screen)
    menu.mainMenu()
