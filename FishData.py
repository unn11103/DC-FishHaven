import random
import math

def randId():
    digits = [i for i in range(0, 10)]
    random_str=""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str

def randCrowdThresh():
    return random.randint(5, 20)

def randPheromoneThresh():
    return random.randint(30, 60)

class FishData:
    def __init__(self, genesis, parentId=None):
        self.id = randId()
        self.state = "in-pond"
        self.status = "alive"
        self.genesis = genesis ## Pond name
        self.crowdThreshold = randCrowdThresh()
        self.pheromone = 0
        self.pheromoneThresh = randPheromoneThresh()
        self.lifetime = 60
        self.parentId = parentId
    def getId(self):
        return self.id
    def getState(self):
        return self.state
    def getStatus(self):
        return self.status
    def getGenesis(self):
        return self.genesis
    def getcrowdThreshold(self):
        return self.crowdThreshold
    def pheromone(self):
        return self.pheromone
    def pheromoneThresh(self):
        return self.pheromoneThresh
    def lifetime(self):
        return self.lifetime
    def parentId(self):
        return self.parentId
    
