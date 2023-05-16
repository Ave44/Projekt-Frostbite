from math import sqrt

from pygame import Vector2
from pygame.mixer import Sound


class SoundPlayer:
    def __init__(self, currentCameraPos: Vector2 = None):
        if currentCameraPos:
            self.currentCameraPos = currentCameraPos
        else:
            self.currentCameraPos = Vector2(0, 0)
        self.maxSoundRange = 1500

    def playSoundWithDistanceEffect(self, sound: Sound, position: Vector2):
        distance = self.currentCameraPos.distance_to(position)
        if distance > self.maxSoundRange:
            return
        volume = 100 - distance/(self.maxSoundRange / 100)
        sound.set_volume(volume / 100)
        sound.play()