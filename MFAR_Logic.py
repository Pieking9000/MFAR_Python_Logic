import random

def main():
    global itemIndex, startingItems, playerItems, remainingLocations, remainingItems, spoilerLogLocations, allLocations
    itemIndex = {
        0:"MorphBall",
        1:"Missile",
        2:"ChargeBeam",
        3:"Bombs",
        4:"HighJump",
        5:"SpeedBooster",
        6:"Varia",
        7:"SuperMissile",
        8:"IceMissle",
        9:"WideBeam",
        10:"PowerBomb",
        11:"SpaceJump",
        12:"PlasmaBeam",
        13:"Gravity",
        14:"WaveBeam",
        15:"DiffusionMissile",
        16:"ScrewAttack",
        17:"IceBeam",
        18:"AnyMissile",
        23:"EnergyTank",
        24:"MissileTank",
        25:"PowerBombTank",
        26:"AnyBomb",
        99:"Undefined"
        }
    #Requirement Baselines
    blueDoors = [[0, 5]]
    greenDoors = [[0, 5], 5, [3, 10], [3, 4]]
    yellowDoors = [[0, 5], 5, [3, 10]]
    redDoors = [[0, 5], 13, 5, [3, 10]]
    anySector = [[0, 5]]
    S1 = [anySector, [[1, 7, 8, 15], 5]]
    S2 = [anySector, [3, 10]]
    anyMissile = [1, 7, 8, 15]
    
    startingItems = [0,1,5,7,8,15]
    remainingItems = [2,3,4,6,9,10,11,12,13,14,16,17]
    playerItems = []
    allLocations = [
        #MainDeck
        Location(0, 9, 4, [[14, [5, 11, [17, 8]]], greenDoors]),
        Location(0, 24, 6, [[1, 7, 8, 15]]),
        Location(0, 25, 6, [[1, 7, 8, 15]]),
        Location(0, 14, 7, [greenDoors, 0, [3, 10]]),
        Location(0, 19, 7, [[1, 7, 8, 15]]),
        Location(0, 20, 7, [[1, 7, 8, 15]]),
        Location(0, 5, 8, [[0, 5], 5]),
        Location(0, 24, 8, [[1, 7, 8, 15]]),
        Location(0, 12, 9, [0]),
        Location(0, 8, 11, [10, [3, 4]]),
        Location(0, 14, 11, [10]),
        Location(0, 21, 16, [[redDoors, 10], 0]),
        Location(0, 22, 18, [[redDoors, 10], 0]),
        Location(0, 21, 21, [[redDoors, 10], 0]),
        Location(0, 5, 22, [redDoors, 14, 5]),
        #Sector 1
        Location(1, 7, 0, [anySector, greenDoors, 11]),
        Location(1, 13, 2, [S1, 0]),
        Location(1, 17, 2, [S1, 0]),
        Location(1, 5, 3, [S1, [11, 5]]),
        Location(1, 6, 3, [S1]),
        Location(1, 7, 4, [S1, 0]),
        Location(1, 9, 4, [S1, 0, 5]),
        Location(1, 10, 4, [S1, anyMissile]),
        Location(1, 9, 6, [S1, anyMissile]),
        Location(1, 12, 7, [S1, 5, 13]),
        Location(1, 13, 8, [S1]),
        Location(1, 1, 9, [S1, 16, 14, anyMissile]),
        Location(1, 4, 10, [S1, 16, 15]),
        Location(1, 8, 11, [S1, 16, 10]),
        #Sector 2
        Location(2, 5, 0, [anySector, 11, 16]),
        Location(2, 5, 1, [anySector, 11, 16]),
        Location(2, 4, 3, [anySector, [4, 5, 16, [8, 17]]]),
        Location(2, 9, 3, [S2, 0]),
        Location(2, 1, 4, [anySector]),
        Location(2, 4, 4, [S2, 0]),
        Location(2, 12, 4, [S2, 0]),
        Location(2, 0, 5, [S2, anyMissile]),
        Location(2, 9, 5, [S2, 0]),
        Location(2, 13, 6, [])
        ]
    remainingLocations = []
    spoilerLogLocations = []
    #test()
    #randomizeMainDeck()
    #printSpoilerLog()
    print(getItemOrder())


def randomizeMainDeck():
    global remainingLocations, playerItems, startingItems, remainingItems, allLocations
    startingItem = startingItems[random.randint(0, len(startingItems) - 1)]
    startingItemLocation = Location(0, 15, 1, [], startingItem)
    startingItemLocation.set_item(startingItem)
    spoilerLogLocations.append(startingItemLocation)
    
    for item in startingItems:
        remainingItems.append(item)
        
    playerItems.append(startingItem)
    remainingItems.remove(startingItem)

    
    #print(itemIndex[startingItem])
    while len(remainingItems) > 0:
        location = allLocations[random.randint(0, len(allLocations) - 1)]
        if canRandoLoc(location):
            tempItem = remainingItems[random.randint(0, len(remainingItems) - 1)]
            playerItems.append(tempItem)
            remainingLocations.extend(getAvailableLocations(tempItem))
            location.set_item(tempItem)
            spoilerLogLocations.append(location)
            remainingItems.remove(tempItem)            
            allLocations.remove(location)


def canRandoLoc(location) -> bool:
    global playerItems
    requirementList = location.itemRequirements
    playerItemsList = playerItems
    canPlayerGetHere = True
    while len(requirementList) > 0:
        for item in playerItemsList:
            for req in requirementList:
                if type(req) is list:
                    for elem in req:
                        if item == elem:
                            requirementList.remove(req)
                else:
                    if item == req:
                        requirementList.remove(req)
        if len(playerItemsList) == 0:
            canPlayerGetHere = False
            break
        else:
            print(len(playerItemsList))
            playerItemsList.remove(item)
    return canPlayerGetHere
                    

def printSpoilerLog():
    global spoilerLogLocations, itemIndex
    for i in range(0, len(spoilerLogLocations) - 1):
        loc = spoilerLogLocations[i]
        print("Item: " + itemIndex[loc.get_item()] + " at S" + str(loc.sector) + "-" + str(loc.X) + "-" + str(loc.Y))

def getAvailableLocations(newItem) -> list:
    global allLocations
    availableLocations = []
    for loc in allLocations:
        for req in loc.itemRequirements:
            if type(req) is list:
                for elem in req:
                    if newItem == elem:
                        availableLocations.append(loc)
            else:
                if newItem == req:
                    availableLocations.append(loc)
    return availableLocations

def getItemOrder() -> list:
    global startingItems, remainingItems
    listOfItems = []
    startingItem = startingItems[random.randint(0, len(startingItems) - 1)]
    listOfItems.append(startingItem)
    startingItems.remove(startingItem)
    remainingItems.extend(startingItems)
    
    while len(remainingItems) > 0:
        nextItem = remainingItems[random.randint(0, len(remainingItems) - 1)]
        listOfItems.append(nextItem)
        remainingItems.remove(nextItem)
    return listOfItems

def test():
    global playerItems
    playerItems = [7, 20]
    testLoc = Location(0, 24, 8, [[1, 7, 8, 15], 0])
    print(canRandoLoc(testLoc))

class Location:
    def __init__(self, sector, X, Y, itemRequirements, itemAtLocation = None):
        self.sector = sector
        self.X = X
        self.Y = Y
        self.itemRequirements = itemRequirements
        self.itemAtLocation = itemAtLocation

    def get_item(self):
        return self.itemAtLocation

    def set_item(self, newItem):
        self.itemAtLocation = newItem

    def set_access(self, access):
        self.playerAccessible = access

    def __str__(self):
        return "S" + str(self.sector) + "-" + str(self.X) + "-" + str(self.Y)


if __name__ == "__main__":
    main()
