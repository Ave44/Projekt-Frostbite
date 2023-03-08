import sys
import random

from pygame import mixer
from pygame.math import Vector2

from config import *
from game.entities.Enemy import Enemy
from game.Menu import Menu
from game.entities.Player import Player
from game.InputManager import InputManager
from game.objects.Grass import Grass
from game.objects.Rock import Rock
from game.objects.Tree import Tree
from game.tiles.Tile import Tile
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

        self.tick = 0

        self.createMap(33)

        inventoryPosition = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60)
        inventory = Inventory(self.UiSprites, 2, 12, inventoryPosition)
        inventory.open()

        self.player = Player(self.visibleSprites,
                             self.obstacleSprites,
                             saveData["player_data"],
                             inventory)

        Enemy(self.visibleSprites,
              self.obstacleSprites,
              saveData["enemy_data"])

        self.UiSprites.player = self.player
        self.UiSprites.inventory = inventory
        self.UiSprites.selectedItem = self.player.selectedItem

        sword = Sword(self.visibleSprites, Vector2(200, 200))
        tree = Tree(self.visibleSprites, self.obstacleSprites, Vector2(3001, 3001), self.clock)
        Rock(self.visibleSprites, self.obstacleSprites, Vector2(3100, 3100))
        Grass(self.visibleSprites, self.obstacleSprites, Vector2(3200, 3200))
        self.player.inventory.addItem(sword, self.player.selectedItem)
        unknownItem = Item(self.visibleSprites, Vector2(200, 200))
        self.player.inventory.addItem(unknownItem, self.player.selectedItem)

        self.InputManager = InputManager(self.player, self.UiSprites, self.visibleSprites)
        self.menu = Menu(screen, self.play, self.options, self.quitGame)

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

    def handleTick(self):
        self.tick = self.tick + 1
        # if self.tick == 60:
            # self.spawnEnemy()
        if self.tick == 120:
            self.tick = 0
            # self.spawnEnemy()
            self.player.heal(20)

    def spawnEnemy(self):
        randomFactor = random.choice([Vector2(1,1),Vector2(-1,1),Vector2(1,-1),Vector2(-1,-1)])
        offset = Vector2(random.randint(128, 512) * randomFactor.x, random.randint(128, 512) * randomFactor.y)
        position = [self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y]
        Enemy(self.visibleSprites, self.obstacleSprites, {
        "speed": 3,
        "maxHealth": 60,
        "currentHealth": 60,
        "damage": 20,
        "sightRange": 400,
        "attackRange": 20,
        "position_center": position,
        "path_to_image_up": "./graphics/player/enemy.png",
        "path_to_image_down": "./graphics/player/enemy.png",
        "path_to_image_left": "./graphics/player/enemy.png",
        "path_to_image_right": "./graphics/player/enemy.png"
    })

    def quitGame(self) -> None:
        pygame.quit()
        sys.exit()

    def mainMenu(self) -> None:
        self.changeMusicTheme(MENU_THEME)
        self.menu.mainMenu()

    def options(self) -> None:
        pass

    def changeMusicTheme(self, theme):
        mixer.music.load(theme)
        mixer.music.play(-1)
        mixer.music.set_volume(MAIN_THEME_VOLUME)

    def entitiesUpdate(self):
        for entity in self.visibleSprites.entities:
            if type(entity) is Enemy:
                entity.searchForTarget(self.visibleSprites.entities)

    def play(self):
        self.changeMusicTheme(HAPPY_THEME)
        while True:
            self.InputManager.handleInput()

            self.entitiesUpdate()

            self.visibleSprites.update()
            self.handleTick()
            self.visibleSprites.customDraw(Vector2(self.player.rect.center))

            self.UiSprites.customDraw()

            # method for debugging values by writing them on screen
            text = f"mx:{pygame.mouse.get_pos()[0]}, my:{pygame.mouse.get_pos()[1]}"
            self.debug(text)

            pygame.display.update()
            self.clock.tick(FPS)
