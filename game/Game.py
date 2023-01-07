import sys

from pygame import mixer
from pygame.math import Vector2

from config import *
from game.entities.Player import Player
from game.InputManager import InputManager
from game.tiles.Tile import Tile
from game.ui.general.Button import Button
from game.ui.inventory.Inventory import Inventory
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.items.Item import Item
from game.items.Sword import Sword
from gameInitialization.GenerateMap import generateMap


class Game:
    def __init__(self, screen, saveData):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.visibleSprites = CameraSpriteGroup()
        self.obstacleSprites = pygame.sprite.Group()
        self.UiSprites = UiSpriteGroup()

        # self.createMap(saveData["world_map"])
        self.createMap(33)

        inventoryPosition = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60)
        inventory = Inventory(self.UiSprites, 2, 12, inventoryPosition)
        inventory.open()

        self.player = Player(self.visibleSprites,
                             self.obstacleSprites,
                             saveData["player_data"],
                             inventory)

        self.UiSprites.player = self.player
        self.UiSprites.inventory = inventory
        self.UiSprites.selectedItem = self.player.selectedItem

        sword = Sword(self.visibleSprites, Vector2(200, 200))
        sword2 = Sword(self.visibleSprites, Vector2(200, 200))
        self.player.inventory.addItem(sword, self.player.selectedItem)
        unknownItem = Item(self.visibleSprites, Vector2(200, 200))
        self.player.inventory.addItem(unknownItem, self.player.selectedItem)

        self.InputManager = InputManager(self.player, self.UiSprites, self.visibleSprites)

    # later will be replaced with LoadGame(savefile) class
    def createMap(self, mapSize):
        map = generateMap(mapSize)
        for y in range(len(map)):
            for x in range(len(map)):
                xPos = x * TILE_SIZE
                yPos = y * TILE_SIZE
                tile = Tile((xPos, yPos), map[y][x]["image"])
                self.visibleSprites.addTile(tile)
                if not map[y][x]["walkable"]:
                    self.obstacleSprites.add(tile)

    def debug(self, text):
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def quitGame(self):
        pygame.quit()
        sys.exit()

    def mainMenu(self) -> None:
        self.changeMusicTheme(MENU_THEME)
        font = pygame.font.Font(BUTTON_FONT, 100)
        menuOptionFont = pygame.font.Font(BUTTON_FONT, 75)
        # TODO: This is suboptimal. If possible replace this loop with a full background image intended for menu.

        background = pygame.image.load("graphics/tiles/walkable/grassland/grassland.png")
        self.screen.fill((255, 255, 255))
        screenWidth, screenHeight = self.screen.get_size()
        imageWidth, imageHeight = background.get_size()

        for x in range(0, screenWidth, imageWidth):
            for y in range(0, screenHeight, imageHeight):
                self.screen.blit(background, (x, y))

        while True:
            mousePos = pygame.mouse.get_pos()
            menuText = font.render("MAIN MENU", True, FONT_MENU_COLOR)
            menuRect = menuText.get_rect(center=(640, 100))
            play_button = Button(pos=(640, 250),
                                 textInput="PLAY",
                                 font=menuOptionFont, baseColor=BASE_BUTTON_COLOR, hoveringColor=WHITE, action=self.play)
            options_button = Button(pos=(640, 400),
                                    textInput="OPTIONS",
                                    font=menuOptionFont, baseColor=BASE_BUTTON_COLOR, hoveringColor=WHITE, action=self.options)
            quit_button = Button(pos=(640, 550),
                                 textInput="QUIT",
                                 font=menuOptionFont, baseColor=BASE_BUTTON_COLOR, hoveringColor=WHITE, action=self.quitGame)

            self.screen.blit(menuText, menuRect)
            menuButtons = [play_button, options_button, quit_button]

            for button in menuButtons:
                button.update(self.screen, mousePos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in menuButtons:
                        if button.checkForInput(mousePos):
                            button.executeAction()

            pygame.display.update()

    def options(self) -> None:
        pass

    def changeMusicTheme(self, theme):
        mixer.music.load(theme)
        mixer.music.play(-1)
        mixer.music.set_volume(MAIN_THEME_VOLUME)

    def play(self):
        self.changeMusicTheme(HAPPY_THEME)
        while True:
            self.InputManager.handleInput()

            self.visibleSprites.update()
            self.visibleSprites.customDraw(Vector2(self.player.rect.center))

            self.UiSprites.customDraw()

            # method for debugging values by writing them on screen
            text = f"mx:{pygame.mouse.get_pos()[0]}, my:{pygame.mouse.get_pos()[1]}"
            self.debug(text)

            pygame.display.update()
            self.clock.tick(FPS)
