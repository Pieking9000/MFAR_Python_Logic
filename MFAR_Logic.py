import random
from enum import Enum

def main():
    global startingItems, playerItems, remainingLocations, remainingItems, spoilerLogLocations, allLocations
    global samus
    global locationsDict
    allLocations = []
    samus = Player()
    
    startingItems = [
        Item.Morph,
        Item.Missile,
        Item.SpeedBooster,
        Item.SuperMissile,
        Item.IceMissile,
        Item.DiffusionMissile]
    
    remainingItems = [
        Item.ChargeBeam,
        Item.Bombs,
        Item.HighJump,
        Item.Varia,
        Item.WideBeam,
        Item.PowerBomb,
        Item.SpaceJump,
        Item.PlasmaBeam,
        Item.Gravity,
        Item.WaveBeam,
        Item.ScrewAttack,
        Item.IceBeam]

    remainingLocations = []
    spoilerLogLocations = []
    getItemOrder()
    #test()


def getItemOrder():
    global samus, allLocations, startingItems, remainingItems, spoilerLogLocations
    startingItem = startingItems[random.randint(0, len(startingItems) - 1)]
    samus.addItem(startingItem)
    refreshLocations()
    startingItems.remove(startingItem)

    spoilerLogLocations.append(Location(0, 15, 1, True))
    spoilerLogLocations[0].set_item(startingItem)
    
    remainingItems.extend(startingItems)
    print("Starting Item: " + startingItem.name)
    refreshLocations()
    #print(len(getReachableLocations()))
    
    while len(remainingItems) > 0:
        remainingLocations = getReachableLocations()
        if(len(remainingLocations) == 0):
            break
        locToRando = remainingLocations[random.randint(0, len(remainingLocations) - 1)]
        itemToPlace = remainingItems[random.randint(0, len(remainingItems) - 1)]

        locToRando.set_item(itemToPlace)
        remainingItems.remove(itemToPlace)
        remainingLocations.remove(locToRando)
        samus.addItem(itemToPlace)
        spoilerLogLocations.append(locToRando)
        refreshLocations()
        
    for i in spoilerLogLocations:
        if(i.bossAtLocation is not None):
            print(str(i.bossAtLocation.name) + ": " + (str(i.get_item().name)))
        else:
            print(str(i) + ": " + str(i.get_item().name))
        

def getReachableLocations() -> list:
    global samus, allLocations
    returnList = []
    for loc in allLocations:
        if loc.itemRequirements == True:
            returnList.append(loc)
    return returnList
        
def test():
    global samus, allLocations
    samus.addItem(Item.Bombs)
    print(samus.playerFlags["hasBomb"])
    samus.removeItem(Item.Bombs)
    samus.addItem(Item.PowerBomb)
    print(samus.playerFlags["hasBomb"])
    samus.removeItem(Item.PowerBomb)
    print(samus.playerFlags["hasBomb"])

def refreshLocations():
    global allLocations, samus, S1, S2
    S1 = (samus.playerFlags["canEnterSectors"] and (samus.playerFlags["hasMissile"] or (Item.SpeedBooster in samus.itemList)))
    S2 = (samus.playerFlags["canEnterSectors"] and samus.playerFlags["hasBomb"])
    
    allLocations = [
        #MainDeck
        #Location(0, 15, 1, True),
        Location(0, 9, 4, (((Item.WaveBeam in samus.itemList) or (Item.SpeedBooster in samus.itemList and Item.SpaceJump in samus.itemList and samus.playerFlags["canFreeze"])) and samus.doorKey["greenDoors"])),
        Location(0, 24, 6, samus.playerFlags["hasMissile"]),
        Location(0, 25, 6, samus.playerFlags["hasMissile"]),
        Location(0, 14, 7, (samus.doorKey["greenDoors"] and (Item.Morph in samus.itemList) and samus.playerFlags["hasBomb"])),
        Location(0, 19, 7, samus.playerFlags["hasMissile"]),
        Location(0, 20, 7, samus.playerFlags["hasMissile"]),
        Location(0, 5, 8, (samus.playerFlags["canEnterSectors"] and (Item.SpeedBooster in samus.itemList))),
        Location(0, 24, 8, samus.playerFlags["hasMissile"]),
        Location(0, 12, 9, (Item.Morph in samus.itemList)),
        Location(0, 8, 11, ((Item.PowerBomb in samus.itemList) and samus.playerFlags["canMorphJump"])),
        Location(0, 14, 11, (Item.PowerBomb in samus.itemList)),
        Location(0, 21, 16, ((samus.doorKey["redDoors"] or (Item.PowerBomb in samus.itemList)) and (Item.Morph in samus.itemList))),
        Location(0, 21, 21, ((samus.doorKey["redDoors"] or (Item.PowerBomb in samus.itemList)) and (Item.Morph in samus.itemList)), Bosses.Yakuza),
        Location(0, 5, 22, (samus.doorKey["redDoors"] and (Item.WaveBeam in samus.itemList) and (Item.SpeedBooster in samus.itemList))),
        #Sector 1,
        Location(1, 7, 0, (samus.playerFlags["canEnterSectors"] and samus.doorKey["greenDoors"] and (Item.SpaceJump in samus.itemList))),
        Location(1, 13, 2, (S1 and (Item.Morph in samus.itemList))),
        Location(1, 17, 2, (S1 and (Item.Morph in samus.itemList))),
        Location(1, 5, 3, (S1 and ((Item.SpaceJump in samus.itemList) or (Item.SpeedBooster in samus.itemList)))),
        Location(1, 6, 3, S1),
        Location(1, 7, 4, (S1 and (Item.Morph in samus.itemList))),
        Location(1, 9, 4, (S1 and (Item.Morph in samus.itemList) and (Item.SpeedBooster in samus.itemList))),
        Location(1, 10, 4, (S1 and samus.playerFlags["hasMissile"])),
        Location(1, 9, 6, (S1 and samus.playerFlags["hasMissile"])),
        Location(1, 12, 7, (S1 and (Item.SpeedBooster in samus.itemList) and (Item.Gravity in samus.itemList))),
        Location(1, 13, 8, S1),
        Location(1, 1, 9, (S1 and (Item.ScrewAttack in samus.itemList) and (Item.WaveBeam in samus.itemList) and samus.playerFlags["hasMissile"])),
        Location(1, 4, 10, (S1 and (Item.ScrewAttack in samus.itemList) and (Item.DiffusionMissile in samus.itemList))),
        Location(1, 8, 11, (S1 and (Item.ScrewAttack in samus.itemList) and (Item.PowerBomb in samus.itemList))),
        #Sector 2
        Location(2, 5, 0, (samus.playerFlags["canEnterSectors"] and (Item.SpaceJump in samus.itemList) and (Item.ScrewAttack in samus.itemList))),
        Location(2, 5, 1, (samus.playerFlags["canEnterSectors"] and (Item.SpaceJump in samus.itemList) and (Item.ScrewAttack in samus.itemList))),
        Location(2, 4, 3, (samus.playerFlags["canEnterSectors"] and ((Item.HighJump in samus.itemList) or (Item.SpeedBooster in samus.itemList) or (Item.ScrewAttack in samus.itemList) or samus.playerFlags["canFreeze"]))),
        Location(2, 9, 3, (S2 and (Item.Morph in samus.itemList) and samus.doorKey["blueDoors"])),
        Location(2, 1, 4, (samus.playerFlags["canEnterSectors"] and samus.doorKey["blueDoors"])),
        Location(2, 4, 4, (S2 and (Item.Morph in samus.itemList))),
        Location(2, 12, 4, (((Item.PowerBomb in samus.itemList) and samus.playerFlags["canEnterSectors"]) or (S2 and Item.SpaceJump))),
        Location(2, 0, 5, (S2 and samus.playerFlags["hasMissile"] and (Item.Morph in samus.itemList))),
        Location(2, 9, 5, (S2 and (Item.Morph in samus.itemList))),
        Location(2, 13, 6, (samus.playerFlags["canEnterSectors"] and (Item.Morph in samus.itemList) and ((Item.PowerBomb in samus.itemList) or (Item.SpaceJump in samus.itemList) or (Item.ScrewAttack in samus.itemList)) and samus.playerFlags["hasBomb"] and samus.playerFlags["hasMissile"]), Bosses.Nettori),
        Location(2, 5, 8, (S2 and samus.playerFlags["canFreeze"] and (Item.Morph in samus.itemList))),
        Location(2, 8, 8, (S2 and (Item.SpaceJump in samus.itemList))),
        Location(2, 5, 10, (S2 and samus.playerFlags["canFreeze"] and (Item.Morph in samus.itemList))),
        Location(2, 4, 11, (S2 and ((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList)))),
        Location(2, 12, 11, (S2 and (Item.Morph in samus.itemList))),
        Location(2, 3, 12, (S2 and (Item.Morph in samus.itemList) and samus.playerFlags["canMorphJump"])),
        Location(2, 16, 12, (S2 and (Item.SpeedBooster in samus.itemList) and (Item.SpaceJump in samus.itemList) and (Item.ScrewAttack in samus.itemList) and samus.playerFlags["hasMissile"])),
        Location(2, 14, 13, (S2 and samus.playerFlags["hasMissile"]), Bosses.Zazabi),
        Location(2, 3, 14, (S2 and (Item.Morph in samus.itemList) and samus.playerFlags["hasBomb"])),
        Location(2, 16, 14, (S2 and (Item.SpeedBooster in samus.itemList) and (Item.ScrewAttack in samus.itemList) and samus.playerFlags["hasMissile"]))
        ]

class Location:
    
    def __init__(self, sector, X, Y, itemRequirements, bossAtLocation = None, itemAtLocation = None):
        self.sector = sector
        self.X = X
        self.Y = Y
        self.itemRequirements = itemRequirements
        self.itemAtLocation = itemAtLocation
        self.bossAtLocation = bossAtLocation

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
        self.missileDamage = 0
        self.flagKey = {
            "hasMissile":[Item.Missile, Item.SuperMissile, Item.IceMissile, Item.DiffusionMissile],
            "hasBomb":[Item.Bombs, Item.PowerBomb],
            "canFreeze":[Item.IceMissile, Item.IceBeam],
            "canMorphJump":[Item.Bombs, Item.HighJump],
            "canEnterSectors":[Item.Morph, Item.SpeedBooster]}
        
        self.playerFlags = {
            #player can have any item in flagKey entry to be True
            "hasMissile":False,
            "hasBomb":False,
            "canFreeze":False,
            "canMorphJump":False,
            "canEnterSectors":False}
        
        self.doorKey = {
            "blueDoors":self.playerFlags["canEnterSectors"],
            "greenDoors": self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and self.playerFlags["hasBomb"] and self.playerFlags["canMorphJump"],
            "yellowDoors":self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and self.playerFlags["hasBomb"] and (Item.Varia in self.itemList),
            "redDoors":self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and (Item.Gravity in self.itemList) and (self.playerFlags["hasBomb"] or (Item.ScrewAttack in self.itemList))}
        
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
            "greenDoors": self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and self.playerFlags["hasBomb"] and self.playerFlags["canMorphJump"],
            "yellowDoors":self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and self.playerFlags["hasBomb"] and (Item.Varia in self.itemList),
            "redDoors":self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and (Item.Gravity in self.itemList) and (self.playerFlags["hasBomb"] or (Item.ScrewAttack in self.itemList))}
        
    def removeItem(self, item):
        self.itemList.remove(item)
        
        self.doorKey = {
            "blueDoors":self.playerFlags["canEnterSectors"],
            "greenDoors": self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and self.playerFlags["hasBomb"] and self.playerFlags["canMorphJump"],
            "yellowDoors":self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and self.playerFlags["hasBomb"] and (Item.Varia in self.itemList),
            "redDoors":self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and (Item.Gravity in self.itemList) and (self.playerFlags["hasBomb"] or (Item.ScrewAttack in self.itemList))}
     
        for entry in self.playerFlags:
            if item in self.flagKey[entry]:
                if self.playerFlags[entry] == True:
                    for i in self.flagKey[entry]:
                        if i in self.itemList:
                            self.playerFlags[entry] = True
                            break
                        self.playerFlags[entry] = False
                        
        

    def getItemList(self):
        return str(self.itemList)

    def giveETank(self):
        self.health = self.health + 100

    def getHealth(self):
        return str(self.health)


class Boss():

    def __init__(self, health, itemToLeave):
        self.health = health
        self.itemToLeave = itemToLeave

class Item(Enum):
    Morph = 0
    Missile = 1
    ChargeBeam = 2
    Bombs = 3
    HighJump = 4
    SpeedBooster = 5
    Varia = 6
    SuperMissile = 7
    IceMissile = 8
    WideBeam = 9
    PowerBomb = 10
    SpaceJump = 11
    PlasmaBeam = 12
    Gravity = 13
    WaveBeam = 14
    DiffusionMissile = 15
    ScrewAttack = 16
    IceBeam = 17
    ETank = 18
    MissileTank = 19
    PowerBombTank = 20
    
class Bosses(Enum):
    Arachnus = Boss(150, [Item.Morph])
    ChargeCoreX = Boss(33, [])
    Zazabi = Boss(100, [Item.HighJump, Item.SpaceJump])
    Serris = Boss(50, [Item.SpeedBooster])
    #BoxOne doesn't count here because the boss' core can't give you an item
    #MegaCoreX also doesn't count because as far as the logic is concerned,
    #it's just a location with base requirements. All special boss logic will
    #be handled by the ASM side of the rando
    #WideCoreX is the same as MegaCoreX, if you can get to the location, you can kill
    #the boss with no health requirements to consider
    Yakuza = Boss(1000, [Item.SpaceJump])
    Nettori = Boss(2000, [])
    Nightmare = Boss(1200, [Item.SpeedBooster, Item.Gravity])
    BoxTwo = Boss(500, [Item.WaveBeam, Item.ScrewAttack])
    Ridley = Boss(4500, [Item.SpaceJump])
    


if __name__ == "__main__":
    main()
