from math import sqrt

from pygame import Vector2
from pygame.mixer import Sound


class SoundPlayer:
    def __init__(self, currentCameraPos: Vector2 = Vector2(0, 0)):
        self.currentCameraPos = currentCameraPos
        self.maxSoundRange = 1000

    def playSoundWithDistanceEffect(self, sound: Sound, position: Vector2):
        distance = self.currentCameraPos.distance_to(position)
        if distance > self.maxSoundRange:
            return
        volume = 1 - (distance / self.maxSoundRange)
        sound.set_volume(volume)
        sound.play()
        