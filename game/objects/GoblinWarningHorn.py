from pygame import Vector2
from pygame.time import Clock

from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.SoundPlayer import SoundPlayer

from game.entities.Goblin import Goblin
from game.items.domain.Hammer import Hammer
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites

from game.items.GoblinFang import GoblinFang


class GoblinWarningHorn(Object):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, midBottom: Vector2,
                 clock: Clock, soundPlayer: SoundPlayer):
        image = loadedImages.goblinHorn
        Object.__init__(self, visibleSprites, midBottom, 50, Hammer, image)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds
        self.numberOfGoblinsToSpawn = 6
        self.obstacleSprites = obstacleSprites
        self.clock = clock
        self.soundPlayer = soundPlayer

    def spawnGoblins(self):
        pos = Vector2(self.rect.centerx, self.rect.centery)
        for i in range(0, self.numberOfGoblinsToSpawn):
            Goblin(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock, pos, self.soundPlayer)

    def interact(self) -> None:
        print("interacted with goblin horn")
        self.spawnGoblins()

    def drop(self) -> None:
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)
