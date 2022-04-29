class PondData:
    def __init__(self, pondName):
        self.pondName = pondName
        self.fishes = []

    def __str__(self):
        fishId = ""
        for f in self.fishes:
            fishId += f.getId() + " "
        return self.pondName + " " + fishId
    
    def addFish(self, fishData):
        self.fishes.append(fishData)

    def getFishById( self, fishId):
        res = None
        for fish in self.fishes:
            if fish.id == fishId:
                return fish

    def setFish( self, newFishData):
        for i in range(len(self.fishes)):
            if self.fishes[i].id == newFishData.id:
                self.fishes[i] = newFishData
                return