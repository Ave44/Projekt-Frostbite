from pygame import Color

from constants import AUTUMN_COLORS, WINTER_COLORS, SPRING_COLORS, SUMMER_COLORS
from game.dayCycle.season.Season import Season


class SeasonController:
    def __init__(self):
        self.seasons = self.createSeasons()
        self.yearLength = sum(season.length for season in self.seasons)

    def getDayPhasesOfCurrentSeason(self, currentDay: int) -> list[tuple[int, Color]]:
        seasonDay = currentDay % self.yearLength
        for idx, season in enumerate(self.seasons):
            seasonEnd = season.length
            if seasonDay <= seasonEnd:
                return season.getDayPhases(seasonDay)
            seasonDay -= seasonEnd

    @staticmethod
    def createSeasons() -> list[Season]:
        autumn = Season([22, 20], [7, 9], 4, 4, 20, 20, AUTUMN_COLORS)
        winter = Season([20, 18], [9, 11], 5, 5, 20, 10, WINTER_COLORS)
        spring = Season([20, 22], [9, 7], 4, 4, 20, 20, SPRING_COLORS)
        summer = Season([22, 24], [7, 5], 3, 3, 20, 10, SUMMER_COLORS)
        seasons = [autumn, winter, spring, summer]
        return seasons
