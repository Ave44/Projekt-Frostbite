from pygame import Surface, Vector2, Rect


class Glowing:
    def __init__(self, image: Surface, spriteRect: Rect, topLeftOffset: Vector2):
        self.lightImage = image
        self.spriteRect = spriteRect
        self.topLeftOffset = topLeftOffset

    def calculateTopLeftPosition(self) -> Vector2:
        return Vector2(self.spriteRect.topleft[0], self.spriteRect.topleft[1]) + self.topLeftOffset
