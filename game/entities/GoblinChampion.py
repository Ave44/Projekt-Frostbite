from pygame import Vector2
from pygame.time import Clock
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.domain.AnimatedEntity import AnimatedEntity

from game.entities.domain.AggressiveMob import AggressiveMob
from game.items.BigMeat import BigMeat
from game.items.GoblinChampionFang import GoblinChampionFang
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class GoblinChampion(AggressiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, clock: Clock, midbottom: Vector2,
                 currHealth: int = None):
        entityData = {
            "speed": 4,
            "maxHealth": 100,
            "damage": 25,
            "sightRange": 150,
            "attackRange": 40
        }
        AggressiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages.GoblinChampion, loadedSounds.GoblinChampion, entityData, clock, 700, 500,
                               1000, 2000, midbottom, currHealth)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds

    def afterAttackAction(self):
        self.playSound(self.soundAttack)

    def drop(self) -> None:
        BigMeat(self.visibleSprites, self.rect.center, self.loadedImages)
        GoblinChampionFang(self.visibleSprites, self.rect.center, self.loadedImages)
