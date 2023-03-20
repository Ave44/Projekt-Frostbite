import pygame
from pygame import Vector2

from config import ROOT_PATH
from game.items.ToolType import ToolType
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class RabbitHole(Object):
    def __init__(self, visibleGroup: CameraSpriteGroup, midBottom: Vector2):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/rabbit_hole.png")
        super().__init__(visibleGroup, midBottom, 50, ToolType.SHOVEL, image)
        self.connectedRabbit = []
        self.hiddenRabbits = []
        self.daysFromConnectedRabbitChange = 0

    def hideRabbit(self, rabbit: Rabbit):
        if len(self.hiddenRabbits) >= 3:
            ValueError("The hole is full")
        self.hiddenRabbits.append(rabbit)
        rabbit.changeStatus(Status.HIDDEN)

    def releaseRabbits(self):
        for rabbit in self.hiddenRabbits:
            rabbit.changeStatus(Status.NORMAL)

    def spawnRabbit(self):
        newRabbit = Rabbit(self.visibleGroup, self.rect.center, self)
        self.connectedRabbit.append(newRabbit)
        self.daysFromConnectedRabbitChange = 0

    def disconnectRabbit(self, rabbit: Rabbit):
        if rabbit in self.connectedRabbit:
            self.connectedRabbit.remove(rabbit)
            self.daysFromConnectedRabbitChange = 0
        else:
            ValueError("Rabbit not found")

    def drop(self) -> None:
        if not self.hiddenRabbits:
            self.spawnRabbit()
        else:
            self.releaseRabbits()

    def interact(self) -> None:
        print("interacted with rabbit hole")

    def handleDayChange(self):
        self.daysFromConnectedRabbitChange += 1

    def update(self):
        if len(self.connectedRabbit) < 3 and self.daysFromConnectedRabbitChange >= 10:
            self.spawnRabbit()
