from pygame import Surface, Vector2


class Tile():
    def __init__(self, position: Vector2, image: Surface):
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.colliderRect = self.rect
