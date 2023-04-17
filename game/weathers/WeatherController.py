from random import random, randint

from pygame import Vector2
from pygame.time import Clock

from Config import Config
from game.LoadedImages import LoadedImages
from game.spriteGroups.WeatherGroup import WeatherGroup
from game.weathers.Rain import Rain
from game.weathers.domain.Weather import Weather


class WeatherController:
    def __init__(self, loadedImages: LoadedImages, clock: Clock,
                 config: Config, weatherGroup: WeatherGroup, weather: Weather = None,
                 weatherDuration: int = 10, currentTime: int = 0):
        self.weatherGroup = weatherGroup
        self.clock = clock
        self.config = config
        self.loadedImages = loadedImages

        self.weather: None | Weather = weather
        self.weatherDuration = weatherDuration
        self.currentTime = currentTime
        self.minWeatherTimeMS = 20000
        self.maxWeatherTimeMs = 60000

        self.offset = Vector2(0, 0)

    def update(self):
        dt = self.clock.get_time()
        self.currentTime += dt

        if self.currentTime > self.weatherDuration:
            self.changeWeather()
        elif self.weather:
            self.weather.animationUpdate()
            self.weatherGroup.weatherImage = self.weather.image

    def changeWeather(self):
        if random() < 0.25:
            self.weather = Rain(self.loadedImages, self.clock, self.config)
        else:
            self.weather = None
        self.currentTime = 0
        self.weatherDuration = randint(self.minWeatherTimeMS, self.maxWeatherTimeMs)
