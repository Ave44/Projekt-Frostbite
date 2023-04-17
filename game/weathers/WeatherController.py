from pygame import SRCALPHA, Surface, Vector2
from pygame.time import Clock

from Config import Config
from game.LoadedImages import LoadedImages
from game.objects.domain.AnimatedObject import AnimatedObject
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.WeatherGroup import WeatherGroup
from game.weathers.domain.Rain import Rain


class WeatherController:
    def __init__(self, loadedImages: LoadedImages, clock: Clock, config: Config, weatherGroup: WeatherGroup, currentWeather: AnimatedObject = None):
        self.weatherGroup = weatherGroup
        self.currentWeather: None | AnimatedObject = Rain(loadedImages, clock, config)
        self.image = self.currentWeather.image

    def update(self):
        if self.currentWeather:
            self.currentWeather.animationUpdate()
            self.image = self.currentWeather.image
            self.weatherGroup.weatherImage = self.image
