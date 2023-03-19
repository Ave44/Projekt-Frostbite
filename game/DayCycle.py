import pygame

def dayCycle(daySeconds):
    isDay = True
    s = pygame.Surface((1920, 1080))
    if (daySeconds < 1800):
        s.set_alpha(daySeconds / 3600 * 256)
    else:
        s.set_alpha((3600 - daySeconds) / 3600 * 256)
    print(daySeconds)
    s.fill((0, 0, 0))
    pygame.display.get_surface().blit(s, (0, 0))