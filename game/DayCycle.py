import pygame

def dayCycle(daySeconds,dayLengthInSeconds):
    #correlated with UI, resolution should somehow be passed into function from game settings, need to ask UI designer
    s = pygame.Surface((1920, 1080))

    #constants
    BEGINNING_OF_NIGHT_TIME = 21 / 24 * dayLengthInSeconds
    NIGHT_TIME = dayLengthInSeconds
    BEGINNING_OF_DAY_TIME = 6/24*dayLengthInSeconds
    DAY_TIME = 9/24*dayLengthInSeconds

    #sunset
    if (daySeconds > BEGINNING_OF_NIGHT_TIME and daySeconds<=NIGHT_TIME):
        alphaValue=(daySeconds - BEGINNING_OF_NIGHT_TIME) / (6/24*dayLengthInSeconds) * 256
        s.set_alpha(alphaValue)
    #sunrise
    elif (daySeconds > BEGINNING_OF_DAY_TIME and daySeconds<=DAY_TIME):
        alphaValue = (DAY_TIME-daySeconds) / (6/24*dayLengthInSeconds) * 256
        s.set_alpha(alphaValue)
    #day time
    elif (daySeconds > DAY_TIME and daySeconds<=BEGINNING_OF_NIGHT_TIME):
        s.set_alpha(0)
    #night time
    else:
        s.set_alpha(128)
    s.fill((0, 0, 0))
    pygame.display.get_surface().blit(s, (0, 0))