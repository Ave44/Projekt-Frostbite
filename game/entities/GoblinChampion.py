from pygame import Vector2
from pygame.time import Clock
from math import sqrt

from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.domain.AggressiveMob import AggressiveMob
from game.items.BigMeat import BigMeat
from game.items.GoblinFang import GoblinFang
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.entities.domain.Entity import Entity
from game.entities.domain.AnimatedEntity import AnimatedEntity
from game.objects.domain.Object import Object


class GoblinChampion(AggressiveMob, AnimatedEntity):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, clock: Clock, midbottom: Vector2,
                 currHealth: int = None):
        entityData = {
            "speed": 3,
            "maxHealth": 100,
            "damage": 20,
            "sightRange": 150,
            "actionRange": 50,
            "moveEveryMs": 700,
            "minMoveTimeMs": 500,
            "maxMoveTimeMs": 1000,
            "attackCooldownMs": 2000
        }
        AggressiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages.goblin, loadedSounds.goblin, entityData, clock, midbottom, currHealth)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds

    def findClosestOtherEntity(self) -> Entity | None:
        closestEntity = None
        closestDistance = float('inf')
        for entity in self.visibleSprites.entities:
            if type(self) == type(entity) or type(entity).__name__ == "Goblin":
                continue
            distance = sqrt((self.rect.centerx - entity.rect.centerx) ** 2 +
                            (self.rect.bottom - entity.rect.bottom) ** 2)
            if distance < closestDistance:
                closestEntity = entity
                closestDistance = distance
        return closestEntity

    def attack(self, target: Entity | Object):
        AggressiveMob.attack(self, target)
        self.playSound(self.soundAttack)

    def drop(self) -> None:
        BigMeat(self.visibleSprites, self.rect.center, self.loadedImages)
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)
