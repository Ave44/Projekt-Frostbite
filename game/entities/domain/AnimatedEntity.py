from pygame import Surface
from pygame.time import Clock
import random

class AnimatedEntity:
    def __init__(self, images: list[Surface], clock: Clock, timeMsBetweenFrames: int):
        self.images = images
        self.lastFrame = len(images)
        self.currFrame = int(random.uniform(0, self.lastFrame))
        self.timeMsBetweenFrames = timeMsBetweenFrames
        self.timeOnFrame = random.uniform(0, timeMsBetweenFrames)
        self.clock = clock

    def nextFrame(self):
        self.currFrame += 1
        self.timeOnFrame = 0
        if self.currFrame == self.lastFrame:
            self.currFrame = 0
        self.image = self.images[self.currFrame]


    def animationUpdate(self):
        self.timeOnFrame += self.clock.get_time()
        if self.timeOnFrame >= self.timeMsBetweenFrames:
            self.nextFrame()
