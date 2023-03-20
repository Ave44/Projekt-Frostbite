import pygame

def dayCycle(daySeconds,dayLengthInSeconds):
    isDay = True
    s = pygame.Surface((1920, 1080))
    beginningOfNightTime = 21 / 24 * dayLengthInSeconds
    nightTime = dayLengthInSeconds
    beginningOfDayTime = 6/24*dayLengthInSeconds
    dayTime = 9/24*dayLengthInSeconds
    if (daySeconds > beginningOfNightTime and daySeconds<=nightTime):
        alphaValue=(daySeconds - beginningOfNightTime) / (6/24*dayLengthInSeconds) * 256
        s.set_alpha(alphaValue)
    elif (daySeconds > beginningOfDayTime and daySeconds<=dayTime):
        alphaValue = (dayTime-daySeconds) / (6/24*dayLengthInSeconds) * 256
        s.set_alpha(alphaValue)
    elif (daySeconds > dayTime and daySeconds<=beginningOfNightTime):
        s.set_alpha(0)
    else:
        s.set_alpha(128)
    s.fill((0, 0, 0))
    pygame.display.get_surface().blit(s, (0, 0))