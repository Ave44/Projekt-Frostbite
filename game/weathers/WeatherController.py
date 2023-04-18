from random import random, randint

from pygame import Vector2
from pygame.time import Clock

from Config import Config
from game.LoadedImages import LoadedImages
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.weathers.Rain import Rain
from game.weathers.domain.Weather import Weather


class WeatherController:
    def __init__(self, loadedImages: LoadedImages, clock: Clock,
                 config: Config, visibleSprites: CameraSpriteGroup, playerPos: Vector2,
                 weather: Weather = None, weatherDuration: int = 10000, currentTime: int = 0):
        self.visibleSprites = visibleSprites
        self.clock = clock
        self.config = config
        self.loadedImages = loadedImages
        self.playerPos = playerPos

        self.weather: None | Weather = weather
        self.weatherDuration = weatherDuration
        self.currentTime = currentTime
        self.minWeatherTimeMS = 20000
        self.maxWeatherTimeMS = 60000

        self.offset = Vector2(0, 0)

    def update(self, newPlayerPos: Vector2):
        dt = self.clock.get_time()
        self.currentTime += dt

        if self.currentTime > self.weatherDuration:
            self.changeWeather()
        if self.weather:
            self.weather.animationUpdate()
            self.calculateWeatherImageOffset(newPlayerPos)

            self.visibleSprites.weather = self.weather.image
            self.visibleSprites.weatherOffset = -self.offset

            self.playerPos = newPlayerPos


    def changeWeather(self):
        if random() < 0.25:
            self.weather = Rain(self.loadedImages, self.clock, self.config)
            self.visibleSprites.weather = self.weather.image
        else:
            self.weather = None
            self.visibleSprites.weather = self.weather

        self.visibleSprites.weatherOffset = Vector2(0, 0)
        self.currentTime = 0
        self.weatherDuration = randint(self.minWeatherTimeMS, self.maxWeatherTimeMS)

    def calculateWeatherImageOffset(self, newPlayerPos: Vector2):
        self.offset -= self.playerPos - newPlayerPos
        self.offset.x = self.offset.x % (self.weather.image.get_width() / 2)
        self.offset.y = self.offset.y % (self.weather.image.get_height() / 2)
