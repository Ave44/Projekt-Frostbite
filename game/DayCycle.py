import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
class DayCycle:
    def __init__(self, daySeconds,dayLengthInSeconds):
        self.daySeconds = daySeconds
        self.dayLengthInSeconds = dayLengthInSeconds
    def runDayCycle(self,clock):
        #update daySeconds
        deltaTime = clock.get_time() / 1000
        self.daySeconds = self.daySeconds + deltaTime
        if self.daySeconds >= self.dayLengthInSeconds:
            self.daySeconds = 0
        print(self.daySeconds)

        #correlated with UI, resolution should somehow be passed into function
        blackSurface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        #constants
        BEGINNING_OF_NIGHT_TIME = 21 / 24 * self.dayLengthInSeconds
        NIGHT_TIME = self.dayLengthInSeconds
        BEGINNING_OF_DAY_TIME = 6/24*self.dayLengthInSeconds
        DAY_TIME = 9/24*self.dayLengthInSeconds

        #sunset
        if (self.daySeconds > BEGINNING_OF_NIGHT_TIME and self.daySeconds<=NIGHT_TIME):
            alphaValue=(self.daySeconds - BEGINNING_OF_NIGHT_TIME) / (6/24*self.dayLengthInSeconds) * 256
            blackSurface.set_alpha(alphaValue)
        #sunrise
        elif (self.daySeconds > BEGINNING_OF_DAY_TIME and self.daySeconds<=DAY_TIME):
            alphaValue = (DAY_TIME-self.daySeconds) / (6/24*self.dayLengthInSeconds) * 256
            blackSurface.set_alpha(alphaValue)
        #day time
        elif (self.daySeconds > DAY_TIME and self.daySeconds<=BEGINNING_OF_NIGHT_TIME):
            blackSurface.set_alpha(0)
        #night time
        else:
            blackSurface.set_alpha(128)
        blackSurface.fill((0, 0, 0))
        pygame.display.get_surface().blit(blackSurface, (0, 0))