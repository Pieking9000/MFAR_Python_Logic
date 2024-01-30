import random, pdb

def main():
    global itemIndex, startingItems, playerItems, remainingLocations, remainingItems, spoilerLogLocations, allLocations, blueDoors, greenDoors, yellowDoors, redDoors, anySector, anyMissile, S1, S2, locDict
    global samus
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
    locDict = {}
    locDictIter = 0
    samus = Player()
    #Requirement Baselines
    anyMissile = [1, 7, 8, 15]
    anyBomb = [3, 10]
    anySector = [0, 5]
    canFreeze = [8, 17]
    morphJump = [3, 4]
    blueDoors = [anySector]
    greenDoors = [anySector, 5, anyBomb, morphJump]
    yellowDoors = [anySector, 5, anyBomb]
    redDoors = [anySector, 13, 5, anyBomb]

    compoundRequirementsKey = (anyMissile,
                               anyBomb,
                               anySector,
                               canFreeze,
                               morphJump,
                               blueDoors,
                               greenDoors,
                               yellowDoors,
                               redDoors)
    #Sector Requirements
    S1 = [anySector, [anyMissile, 5]]
    # [[[0,5], [1, 7, 8, 15], 5] , 0]
    S2 = [anySector, [3, 10]]
    
    startingItems = [0,1,5,7,8,15]
    remainingItems = [2,3,4,6,9,10,11,12,13,14,16,17]
    playerItems = []
    allLocations = [
        #MainDeck
        Location(0, 9, 4, [[14, [5, 11, canFreeze]], greenDoors]),
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
        Location(2, 4, 3, [anySector, [4, 5, 16, canFreeze]]),
        Location(2, 9, 3, [S2, 0]),
        Location(2, 1, 4, [anySector]),
        Location(2, 4, 4, [S2, 0]),
        Location(2, 12, 4, [S2, 0]),
        Location(2, 0, 5, [S2, anyMissile]),
        Location(2, 9, 5, [S2, 0])
        #Location(2, 13, 6, [])
        ]
    remainingLocations = []
    spoilerLogLocations = []
    test()
    #randomizeMainDeck()
    #printSpoilerLog()
    #print(getItemOrder())


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

def printSpoilerLog():
    global spoilerLogLocations, itemIndex
    for i in range(0, len(spoilerLogLocations) - 1):
        loc = spoilerLogLocations[i]
        print("Item: " + itemIndex[loc.get_item()] + " at S" + str(loc.sector) + "-" + str(loc.X) + "-" + str(loc.Y))

def getAvailableLocations() -> list:
    global allLocations
    availLoc = []
    for loc in allLocations:
        #print(loc)
        if canRandoLoc(loc) == True:
            availLoc.append(loc)
    return availLoc
            

def getItemOrder() -> list:
    global startingItems, remainingItems
    listOfItems = []
    startingItem = startingItems[random.randint(0, len(startingItems) - 1)]
    listOfItems.append(startingItem)
    startingItems.remove(startingItem)
    remainingItems.extend(startingItems)
    
    while len(remainingItems) > 0:
        nextItem = remainingItems[random.randint(0, len(remainingItems) - 1)]
        print(remainingItems)
        listOfItems.append(nextItem)
        remainingItems.remove(nextItem)
    return listOfItems

def test():
    global samus
    samus.addItem(0)
    samus.addItem(15)
    samus.addItem(3)
    samus.addItem(5)
    samus.addItem(17)
    samus.addItem(13)
    print("Current health: " + str(samus.playerFlags))
    #testLoc = Location(1, 13, 2, [[[0, 5], [[1, 7, 8, 15], 5]] , 0])
    #print(canRandoLoc(testLoc))
    #for loc in getAvailableLocations():
    #   print(loc)
    #print(processList(testLoc.itemRequirements))

def processList(listToProcess):
    global playerItems
    reqList = {}
    
    for i in listToProcess:
        reqList[str(i)] = False
    print(reqList)

def meetsRequirement(listToCheck):
    global playerItems
    for item in listToCheck:
        if item in playerItems:
            return True
    return False
   
def canRandoLoc(location) -> bool:
    global locDict
    reqList = []
    for item in location.baseReq:
        if type(item) is list:
            processList(item)
            #print("Dict: " + str(locDict))
        else:
            reqList.append(item in playerItems)
    
    for elem in reqList:
        if elem == False:
            return False
    return True

class Location:
    '''
        ANTIQUATED (This is hopefully going to be handled
        by the player object in conjunction with a basic
        requirementList passed to every location object.
        That list is going to be made up of playerFlags
        that will match exactly with the self.playerFlags
        for easy lookup i.e. The basic requirement list
        can look like [hasMorphJump, canFreeze, 11, redDoors]
        and the logic will check if each req is a flag or an item.
        If flag, will check samus.playerFlags[] to see if the requirement
        is met. If number, will check if number in samus.itemList[]):
        Nested item requirements are optional
        i.e. To get to any sector, you need either
        SpeedBooster or MorphBall, so to express
        that in the itemRequirements field, your final
        list of itemRequirements would be [[0,5]].
        [] is your total list, and [0,5] (Speed Booster
        or Morph ball), is your only requirement
        Another example, to get to the item at coord (13, 5)
        (The Hornoad Hole? I think?) your item requirements would
        look like this: [[0,5], [5, [1, 7, 8, 15]], 0].
        To reach this item, you only need 3 items, your first
        is either morph ball or speed booster to get to the sector
        elevator, the second is either Speed booster or any missile
        to get past the missile barrier before the first atmo room
        (and the atmo room itself), and the third item is morph ball
        and only morph ball
    '''
    def __init__(self, sector, X, Y, baseReq, itemAtLocation = None, sectorReq = [], compReq = []):
        self.sector = sector
        self.X = X
        self.Y = Y
        self.baseReq = baseReq
        self.itemAtLocation = itemAtLocation
        self.sectorReq = sectorReq
        self.compReq = compReq

    def get_item(self):
        return self.itemAtLocation

    def set_item(self, newItem):
        self.itemAtLocation = newItem

    def set_access(self, access):
        self.playerAccessible = access

    def __str__(self):
        return "S" + str(self.sector) + "-" + str(self.X) + "-" + str(self.Y)

class Player:

    def __init__(self):
        self.itemList = []
        self.health = 99
        self.flagKey = {
            "hasMissile":[1, 7, 8, 15],
            "hasBomb":[3, 10],
            "canFreeze":[8, 17],
            "canMorphJump":[3, 4],
            "canEnterSectors":[0, 5]}
        
        self.playerFlags = {
            #player can have any item in flagKey entry to be True
            "hasMissile":False,
            "hasBomb":False,
            "canFreeze":False,
            "canMorphJump":False,
            "canEnterSectors":False}
        
        self.doorKey = {
            "blueDoors":self.playerFlags["canEnterSectors"],
            "greenDoors": self.playerFlags["canEnterSectors"] and 5 in self.itemList and self.playerFlags["hasBomb"] and self.playerFlags["canMorphJump"],
            "yellowDoors":self.playerFlags["canEnterSectors"] and 5 in self.itemList and self.playerFlags["hasBomb"],
            "redDoors":self.playerFlags["canEnterSectors"] and 5 in self.itemList and 13 in self.itemList and self.playerFlags["hasBomb"]}
        
    def setHasMissiles(self, value):
        self.playerFlags["hasMissile"] = value

    def setHasBomb(self, value):
        self.playerFlags["hasBomb"] = value

    def setCanFreeze(self, value):
        self.playerFlags["canFreeze"] = value

    def setCanMorphJump(self, value):
        self.playerFlags["canMorphJump"] = value

    def setCanEnterSectors(self, value):
        self.playerFlags["canEnterSectors"] = value

    def setBlueDoors(self, value):
        self.playerFlags["blueDoors"] = value

    def setGreenDoors(self, value):
        self.playerFlags["greenDoors"] = value

    def setYellowDoors(self, value):
        self.playerFlags["yellowDoors"] = value

    def setRedDoors(self, value):
        self.playerFlags["redDoors"] = value

    def addItem(self, item):
        self.itemList.append(item)
        for entry in self.playerFlags:
            if item in self.flagKey[entry]:
                self.playerFlags[entry] = True

        self.doorKey = {
            "blueDoors":self.playerFlags["canEnterSectors"],
            "greenDoors": self.playerFlags["canEnterSectors"] and 5 in self.itemList and self.playerFlags["hasBomb"] and self.playerFlags["canMorphJump"],
            "yellowDoors":self.playerFlags["canEnterSectors"] and 5 in self.itemList and self.playerFlags["hasBomb"],
            "redDoors":self.playerFlags["canEnterSectors"] and 5 in self.itemList and 13 in self.itemList and self.playerFlags["hasBomb"]}
        
    def removeItem(self, item):
        self.itemList.remove(self.itemList.index(item))

    def getItemList(self):
        return str(self.itemList)

    def giveETank(self):
        self.health = self.health + 100

    def getHealth(self):
        return str(self.health)

if __name__ == "__main__":
    main()
