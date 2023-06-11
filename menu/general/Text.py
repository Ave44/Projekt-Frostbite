from pygame import Color, Surface
from pygame.font import Font

class Text:
    def __init__(self, center: tuple[int, int], text: str, font: Font, color: Color):
        self.surface = font.render(text, True, color)
        self.rect = self.surface.get_rect(center=center)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.surface, self.rect)
