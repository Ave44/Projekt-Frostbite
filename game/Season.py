class Season():
    def __init__(self, dawnStart: list[int, int], dayStart: list[int, int], duskStart: list[int, int],
                 nightStart: list[int, int], length):
        # self.dawnStartDefault = dawnStart[0]
        # self.dawnStartPeak = dawnStart[1]
        # self.dawnStartDiff = self.dawnStartDefault - self.dawnStartPeak

        self.dayStartDefault = dayStart[0]
        self.dayStartPeak = dayStart[1]
        self.dayStartDiff = self.dayStartDefault - self.dayStartPeak

        # self.duskStartDefault = duskStart[0]
        # self.duskStartPeak = duskStart[1]
        # self.duskStartDiff = self.duskStartDefault - self.duskStartPeak

        self.nightStartDefault = nightStart[0]
        self.nightStartPeak = nightStart[1]
        self.nightStartDiff = self.nightStartDefault - self.nightStartPeak

        self.nightLengthDefault = 7
        self.nightLengthPeak = 4

        self.dawnLength = 3
        self.duskLength = 3

        self.length = length
        self.halfLength = length / 2

    # def getDayPhases(self, seasonDay: int):
    #     if seasonDay < self.halfLength:
    #         growthModifier = seasonDay / self.halfLength
    #     else:
    #         growthModifier = 2 - seasonDay / self.halfLength
        
    #     dawnStart = round(self.dawnStartDefault - self.dawnStartDiff * growthModifier)
    #     dayStart = round(self.dayStartDefault - self.dayStartDiff * growthModifier)
    #     duskStart = round(self.duskStartDefault - self.duskStartDiff * growthModifier)
    #     nightStart = round(self.nightStartDefault - self.nightStartDiff * growthModifier)
    #     print(seasonDay, growthModifier,
    #         [dawnStart, self.dawnStartDefault - self.dawnStartDiff * growthModifier, "|",
    #            dayStart, self.dayStartDefault - self.dayStartDiff * growthModifier, "|",
    #            duskStart, self.duskStartDefault - self.duskStartDiff * growthModifier, "|",
    #            nightStart, self.nightStartDefault - self.nightStartDiff * growthModifier])
    #     return [dawnStart, dayStart, duskStart, nightStart]

    
    def getDayPhases(self, seasonDay: int):
        if seasonDay < self.halfLength:
            growthModifier = seasonDay / self.halfLength
        else:
            growthModifier = 2 - seasonDay / self.halfLength
        
        nightStart = round(self.nightStartDefault - self.nightStartDiff * growthModifier)
        nightLength = round(self.nightLengthDefault - self.nightLengthPeak * growthModifier)

        dawnStart = (nightStart + nightLength) % 24
        dayStart = dawnStart + self.dawnLength
        duskStart = nightStart - self.duskLength


        print(dawnStart, dayStart, duskStart, nightStart, "|", seasonDay, growthModifier)
        return [dawnStart, dayStart, duskStart, nightStart]