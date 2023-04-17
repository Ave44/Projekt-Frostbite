from pygame import display, Vector2, Surface


class WeatherGroup:
    def __init__(self, playerCenter: Vector2, weatherImage: Surface = None, offset: Vector2 = Vector2(0, 0)):
        self.displaySurface = display.get_surface()
        self.playerCenter = playerCenter
        self.weatherImage = weatherImage
        self.offset = Vector2(0, 0)
        if self.weatherImage:
            self.offset = Vector2(self.weatherImage.get_width() / 2, self.weatherImage.get_height() / 2)

    def changeWeatherImage(self, newWeatherImage: Surface):
        self.weatherImage = newWeatherImage
        self.offset = Vector2(self.weatherImage.get_width() / 2, self.weatherImage.get_height() / 2)

    def customDraw(self, newPlayerCenter: Vector2):
        if not self.weatherImage:
            return
        self.displaySurface.blit(self.weatherImage, -self.offset)
        self.offset -= self.playerCenter - newPlayerCenter
        self.offset.x = self.offset.x % (self.weatherImage.get_width() / 2)
        self.offset.y = self.offset.y % (self.weatherImage.get_height() / 2)
        self.playerCenter = newPlayerCenter
