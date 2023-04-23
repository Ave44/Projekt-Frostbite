from pygame import Color

from math import floor, ceil

class Season():
    def __init__(self, nightStart: list[int, int], nightLength: list[int, int],
                 dawnLength: int, duskLength: int, seasonLength: int, peakDay: int,
                 clockColors: list[Color]):

        self.nightStartDefault = nightStart[0]
        self.nightStartPeak = nightStart[1]
        self.nightStartDiff = self.nightStartDefault - self.nightStartPeak

        self.nightLengthDefault = nightLength[0]
        self.nightLengthPeak = nightLength[1]
        self.nightLengthDiff = self.nightLengthDefault - self.nightLengthPeak

        self.dawnLength = dawnLength
        self.duskLength = duskLength

        self.length = seasonLength
        self.peakDay = peakDay
        self.colors = clockColors

    def getDayPhases(self, seasonDay: int, daySegmentLengthMs: int) -> list[dict[int, Color]]:
        if seasonDay < self.peakDay:
            growthModifier = seasonDay / self.peakDay
        else:
            growthModifier = 2 - seasonDay / self.peakDay
        
        nightStart = self.customRound(self.nightStartDefault - self.nightStartDiff * growthModifier, self.nightStartDiff)
        nightLength = self.customRound(self.nightLengthDefault - self.nightLengthDiff * growthModifier, self.nightLengthDiff)

        dawnStart = (nightStart + nightLength) % 24
        dayStart = (dawnStart + self.dawnLength) % 24
        duskStart = nightStart - self.duskLength

        dayPhases = [dawnStart, dayStart, duskStart, nightStart]
        for phaseIndex in range(len(dayPhases)):
            dayPhases[phaseIndex] = {'start': dayPhases[phaseIndex] * daySegmentLengthMs, 'color': self.colors[phaseIndex]}

        return dayPhases

    def customRound(self, number: float, numberChangeStep: float) -> int:
        if numberChangeStep > 0:
            return floor(number + 0.5)
        return ceil(number - 0.5)
