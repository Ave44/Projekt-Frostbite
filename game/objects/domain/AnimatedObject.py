from pygame import Surface
from pygame.time import Clock
import random


class AnimatedObject:
    def __init__(self, images: list[Surface], clock: Clock, timeMsBetweenFrames: int):
        self.numberOfImages = len(images)
        self.images = images
        self.currFrameIndex = int(random.uniform(0, self.numberOfImages))
        self.timeMsBetweenFrames = timeMsBetweenFrames

        self.image = images[self.currFrameIndex]
        self.timeOnFrame = 0
        self.clock = clock

    def nextFrame(self):
        self.currFrameIndex = (self.currFrameIndex + 1) % self.numberOfImages
        self.timeOnFrame = 0
        self.image = self.images[self.currFrameIndex]

    def animationUpdate(self):
        self.timeOnFrame += self.clock.get_time()
        if self.timeOnFrame >= self.timeMsBetweenFrames:
            self.nextFrame()
