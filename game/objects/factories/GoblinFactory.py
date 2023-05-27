from pygame.time import Clock

from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.SoundPlayer import SoundPlayer
from game.entities.Goblin import Goblin
from game.entities.GoblinChampion import GoblinChampion
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class GoblinFactory:
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds,
                 clock: Clock, soundPlayer: SoundPlayer):
        self.visibleSprites = visibleSprites
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds
        self.obstacleSprites = obstacleSprites
        self.clock = clock
        self.soundPlayer = soundPlayer

    def createGoblin(self, pos, currHealth: int | None = None) -> Goblin:
        newGoblin = Goblin(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock,
                           pos, self.soundPlayer, currHealth)
        return newGoblin

    def createGoblinChampion(self, pos, currHealth: int | None = None) -> GoblinChampion:
        newGoblinChampion = GoblinChampion(self.visibleSprites, self.obstacleSprites, self.loadedImages,
                                           self.loadedSounds, self.clock, pos, self.soundPlayer, currHealth)
        return newGoblinChampion
