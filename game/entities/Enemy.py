import pygame
from pygame.math import Vector2
import math
import random

from game.entities.Entity import Entity


class Enemy(Entity):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 obstacleSprites: pygame.sprite.Group,
                 enemyData):
        super().__init__(groups, obstacleSprites, enemyData)
        self.sightRange = enemyData["sightRange"]
        self.attackRange = enemyData["attackRange"]
        self.damage = enemyData["damage"]
        self.target = None
        self.visibleSprites = groups
        self.id = random.randint(00000000, 99999999)

    def isInSightRange(self, position: tuple[int, int]) -> bool:
        return self.isInRange(self.sightRange, position)

    def isInAttackRange(self, position: tuple[int, int]) -> bool:
        return self.isInRange(self.attackRange, position)

    def isInRange(self, range: int, position: tuple[int, int]) -> bool:
        pos = Vector2(position)
        distance = math.sqrt((self.rect.centerx - pos.x)**2 + (self.rect.centery - pos.y)**2)
        return distance <= range


    def searchForTarget(self, entities):
        if self.target != None:
            if not self.isInSightRange(self.target.rect.center):
                self.target = None
                self.destinationPosition = None
        else:
            for entity in entities:
                if type(entity) != type(self):
                    if self.isInSightRange(entity.rect.center):
                        self.target = entity
                        break

    def attack(self):
        if self.isInSightRange(self.target.rect.center):
            self.destinationPosition = Vector2(self.target.rect.midbottom)
        if self.isInAttackRange(self.target.rect.center):
            self.target.getDamage(self.damage)
            self.kill()

    def update(self):
        # print(self.target)
        if self.target != None:
            self.attack()
            self.visibleSprites.addRadius(self.sightRange, self.rect.center)
            self.visibleSprites.addRadius(self.attackRange, self.rect.center)
        self.move()
