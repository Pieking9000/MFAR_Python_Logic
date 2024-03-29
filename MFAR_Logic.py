import random, json
from enum import Enum

def main():
    global startingItems, playerItems, remainingLocations, remainingItems, spoilerLogLocations, tankLocations, allSectors, missileFirstPath, extraItemLocations
    global samus
    global randomizer
    allSectors = []
    missileFirstPath = []
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

    tankLocations = []

    remainingLocations = []
    spoilerLogLocations = []
    getItemOrder()
    placeTanks()
    #printSpoilerLog()
    writeSpoilerLog()
    #test()


def getItemOrder():
    global samus, startingItems, remainingItems, spoilerLogLocations, missileFirstPath
    startingItem = startingItems[random.randint(0, len(startingItems) - 1)]
    samus.addItem(startingItem)
    refreshLocations()
    startingItems.remove(startingItem)

    spoilerLogLocations.append(Location(0, 15, 1, True, dataRoom = True))
    spoilerLogLocations[0].set_item(startingItem)
    
    remainingItems.extend(startingItems)

    if samus.playerFlags["hasMissile"]:
        morphLocation = missileFirstPath[random.randint(0, len(missileFirstPath) - 1)]
        samus.addItem(Item.Morph)
        morphLocation.set_item(Item.Morph)
        spoilerLogLocations.append(morphLocation)
        remainingItems.remove(Item.Morph)
        
    refreshLocations()
    canContinue = True
    
    while len(remainingItems) > 0: # and canContinue == True:
        reachableLocations = getReachableLocations()
        hasAllLeaveRequirements = True
        
        if(len(reachableLocations) == 0):
            canContinue = False  
        elif len(reachableLocations) == 1:
            locToRando = reachableLocations[0]
        else:
            #print("Length of reachableLocations: " + str(len(reachableLocations)))
            locToRando = reachableLocations[random.randint(0, len(reachableLocations) - 1)]
            
        itemToPlace = remainingItems[random.randint(0, len(remainingItems) - 1)]

        while locToRando in spoilerLogLocations:
            shouldReroll = False
            for i in reachableLocations:
                if i not in spoilerLogLocations:
                    shouldReroll = True
            if shouldReroll:
                if len(reachableLocations) == 1:
                    locToRando = reachableLocations[0]
                else:
                    locToRando = reachableLocations[random.randint(0, len(reachableLocations) - 1)]
            else:
                #print("All reachable locations used")
                canContinue = False
                break

        if locToRando.bossAtLocation is not None:
            hasAllLeaveRequirements = False
            if len(locToRando.bossAtLocation.value.itemToLeave) > 0:
                for i in locToRando.bossAtLocation.value.itemToLeave:
                    if i not in samus.itemList:
                        hasAllLeaveRequirements = False
                        canContinue = False
                        break
                    else:
                        hasAllLeaveRequirements = True
            else:
                hasAllLeaveRequirements = True

        if canContinue:
            locToRando.set_item(itemToPlace)
            remainingItems.remove(itemToPlace)
            samus.addItem(itemToPlace)
            spoilerLogLocations.append(locToRando)
            refreshLocations()
        else:
            #print(samus.itemList)
            lastItemAdded = samus.itemList[-1]
            remainingItems.append(lastItemAdded)
            samus.removeItem(lastItemAdded)
            lastLocation = spoilerLogLocations[-1]
            spoilerLogLocations.remove(lastLocation)
            canContinue = True
            refreshLocations()
            #print("Trying again")

def placeTanks():
    global allSectors, tankLocations, spoilerLogLocations

    tankableLocations = []
    ETanks = 0 #20
    Missiles = 0 #48
    PB = 0 #32

    for i in allSectors:
        for j in i.itemLocations:
            if j not in spoilerLogLocations:
                tankableLocations.append(j)

    while ETanks < 20 and Missiles < 48 and PB < 32:
        locToRando = tankableLocations[random.randint(0, len(tankableLocations) - 1)]
        whatToPlace = random.randint(0, 2)
        if whatToPlace == 0 and ETanks < 20:
            locToRando.set_item(Item.ETank)
            tankLocations.append(locToRando)
            tankableLocations.remove(locToRando)
            ETanks = ETanks + 1
        elif whatToPlace == 1 and Missiles < 48:
            locToRando.set_item(Item.MissileTank)
            tankLocations.append(locToRando)
            tankableLocations.remove(locToRando)
            Missiles = Missiles + 1
        elif whatToPlace == 2 and PB < 32:
            locToRando.set_item(Item.PowerBombTank)
            tankLocations.append(locToRando)
            tankableLocations.remove(locToRando)
            PB = PB + 1
            
    


def printSpoilerLog():
    global spoilerLogLocations, randomizer
    
    for i in spoilerLogLocations:
        if(i.bossAtLocation is not None):
            print(str(i.bossAtLocation.name) + ": " + str(i.itemAtLocation.name))
        elif i.dataRoom:
            print("Data S" + str(i.sector) + ": " + str(i.itemAtLocation.name))
        else:
            if randomizer.showCommNames == True:
                print("S" + str(i.sector) + "-" + i.commName + ": " + str(i.itemAtLocation.name))
            else:
                print(str(i) + ": " + str(i.itemAtLocation.name))
            

def writeSpoilerLog():
    global spoilerLogLocations, randomizer, extraItemLocations, tankLocations
    mainItems = {}
    tanks = {}
    settings = {
        "Difficulty": randomizer.difficulty,
        "Major/Minor Item Split": randomizer.majMinItemSplit,
        "Missile Upgrades Enable Missiles": randomizer.missileUpgradesEnableMissiles,
        "Use Power Bombs Without Bombs": randomizer.bombsEnablePB,
        "Damage Runs": randomizer.damageRuns,
        "Split Security Levels": randomizer.splitSecurityLevels,
        "Sector Shuffle": randomizer.sectorShuffle,
        "Show Community Names": randomizer.showCommNames        
        }
    
    for i in spoilerLogLocations:
        if(i.bossAtLocation is not None):
            mainItems[str(i.bossAtLocation.name)] = str(i.itemAtLocation.name)
        elif i.dataRoom:
            mainItems["Data S" + str(i.sector)] = str(i.itemAtLocation.name)
        else:
            if randomizer.showCommNames == True:
                mainItems["S" + str(i.sector) + "-" + i.commName] = str(i.itemAtLocation.name)
            else:
                mainItems[str(i)] = str(i.itemAtLocation.name)

    for i in tankLocations:
        if(i.bossAtLocation is not None):
            tanks[str(i.bossAtLocation.name)] = str(i.itemAtLocation.name)
        elif i.dataRoom:
            tanks["Data S" + str(i.sector)] = str(i.itemAtLocation.name)
        else:
            if randomizer.showCommNames == True:
                tanks["S" + str(i.sector) + "-" + i.commName] = str(i.itemAtLocation.name)
            else:
                tanks[str(i)] = str(i.itemAtLocation.name)
        
    finalLog = {
        "Settings": settings,
        "Main Items": mainItems,
        "Tank Locations": tanks
        }
    
    json_object = json.dumps(finalLog, indent=4)

    with open("testLog.json", "w") as outfile:
        outfile.write(json_object)
    
 

def getReachableLocations() -> list:
    global samus, allSectors
    returnList = []
    for i in allSectors:
        if i.doorReq == True:
            for loc in i.itemLocations:
                if loc.itemRequirements == True:
                    returnList.append(loc)
        else:
            continue
    return returnList
        
def test():
    global samus, allSectors
    print(len(Bosses.WideCoreX.value.itemToLeave))


def refreshLocations():
    global allSectors, samus, missileFirstPath
    S1 = (samus.playerFlags["canEnterSectors"] and (samus.playerFlags["hasMissile"] or (Item.SpeedBooster in samus.itemList)))
    S2 = (samus.playerFlags["canEnterSectors"] and samus.playerFlags["hasBomb"])
    S3 = (samus.playerFlags["canEnterSectors"])
    #This definition of S4 accounts for the players ability to exit S4 but not sure if I want to include this
    #since nothing will be in S4 unless you can already leave, including items that allow you
    #to leave. For example, one way to leave S4 is with speed booster and lowering the water level
    #With this definition, Speedbooster will never be in S4. Essentially, this trades seed spiciness for
    #less softlocks
    #S4 = (samus.playerFlags["canEnterSectors"] and samus.playerFlags["hasBomb"] and ((samus.doorKey["blueDoors"] and (Item.SpeedBooster in samus.itemList)) or ((Item.SpaceJump in samus.itemList) or ((Item.HighJump in samus.itemList) and samus.playerFlags["canFreeze"])))))
    S4 = (samus.playerFlags["canEnterSectors"] and samus.playerFlags["hasBomb"])
    #Broken Sector 5 Logic
    BS5NoGrav = ((Item.Varia in samus.itemList) and (Item.WaveBeam in samus.itemList) and (Item.HighJump in samus.itemList) and samus.doorKey["yellowDoors"])
    BS5Grav = ((Item.Varia in samus.itemList) and (Item.Gravity in samus.itemList) and (Item.SpeedBooster in samus.itemList))
    BS5RedDoors = ((Item.Gravity in samus.itemList) and (Item.SpeedBooster in samus.itemList) and samus.doorKey["redDoors"])
    BS5 = (BS5NoGrav or BS5Grav or BS5RedDoors)
    #Lower Sector 4
    LS4 = (samus.playerFlags["canEnterSectors"] and (Item.SpeedBooster in samus.itemList) and (Item.Gravity in samus.itemList) and BS5)
    S5 = (samus.playerFlags["canEnterSectors"] and (Item.Varia in samus.itemList) and (((Item.Morph in samus.itemList) and samus.playerFlags["hasMissile"]) or samus.doorKey["yellowDoors"]))
    S6 = (samus.playerFlags["canEnterSectors"] and (Item.Varia in samus.itemList) and ((Item.SpeedBooster in samus.itemList) or (Item.SuperMissile in samus.itemList) or (Item.PowerBomb in samus.itemList) or (Item.ScrewAttack in samus.itemList)))

    missileFirstPath = [
        Location(0, 24, 6, (samus.playerFlags["hasMissile"] and (Item.Morph in samus.itemList)), commName = "Arachnus E-Tank"),
        Location(0, 25, 6, (samus.playerFlags["hasMissile"] and (Item.Morph in samus.itemList)), commName = "The Attic"),
        Location(0, 19, 7, (samus.playerFlags["hasMissile"] and (Item.Morph in samus.itemList)), commName = "Second Missiles"),
        Location(0, 20, 7, (samus.playerFlags["hasMissile"] and (Item.Morph in samus.itemList)), commName = "First Missiles"),
        Location(0, 24, 8, samus.playerFlags["hasMissile"], bossAtLocation = Bosses.Arachnus),
        ]
    
    mainDeckLocations = [Location(0, 9, 4, (((Item.WaveBeam in samus.itemList) or (Item.SpeedBooster in samus.itemList and Item.SpaceJump in samus.itemList and samus.playerFlags["canFreeze"])) and samus.doorKey["greenDoors"]), commName = "Animals"),
        Location(0, 14, 7, (samus.doorKey["greenDoors"] and (Item.Morph in samus.itemList) and samus.playerFlags["hasBomb"]), commName = "Behind PB Geron"),
        Location(0, 5, 8, (samus.playerFlags["canEnterSectors"] and (Item.SpeedBooster in samus.itemList)), commName = "Main Elevator"),
        Location(0, 12, 9, (Item.Morph in samus.itemList), commName = "Cubby Hole"),
        Location(0, 8, 11, ((Item.PowerBomb in samus.itemList) and samus.playerFlags["canMorphJump"]), commName = "Maintenance Tunnel"),
        Location(0, 14, 11, (Item.PowerBomb in samus.itemList) and (Item.Morph in samus.itemList), commName = "Spitter Hallway East"),
        Location(0, 21, 16, ((samus.doorKey["redDoors"] or (Item.PowerBomb in samus.itemList)) and (Item.Morph in samus.itemList)), commName = "Reactor E-Tank"),
        Location(0, 22, 18, ((samus.doorKey["redDoors"] or (Item.PowerBomb in samus.itemList)) and (Item.Morph in samus.itemList)), commName = "Reactor Missiles"),
        Location(0, 21, 21, ((samus.doorKey["redDoors"] or (Item.PowerBomb in samus.itemList)) and (Item.Morph in samus.itemList)), Bosses.Yakuza),
        Location(0, 5, 22, (samus.doorKey["redDoors"] and (Item.WaveBeam in samus.itemList) and (Item.SpeedBooster in samus.itemList)), commName = "In Space")
        ]

    S1Locations = [Location(1, 7, 0, (samus.playerFlags["canEnterSectors"] and samus.doorKey["greenDoors"] and (Item.SpaceJump in samus.itemList)), commName = "Antechamber"),
        Location(1, 13, 2, (S1 and (Item.Morph in samus.itemList)), commName = "Hornoad Hole"),
        Location(1, 17, 2, (S1 and (Item.Morph in samus.itemList)), commName = "Baby's First Wall Jump"),
        Location(1, 5, 3, (S1 and ((Item.SpaceJump in samus.itemList) or (Item.SpeedBooster in samus.itemList))), commName = "Lava Dive (Far)"),
        Location(1, 6, 3, S1, commName="Lava Dive (Near)"),
        Location(1, 7, 4, (S1 and (Item.Morph in samus.itemList)), commName = "Lava Dive (Bottom)"),
        Location(1, 9, 4, (S1 and (Item.Morph in samus.itemList) and (Item.SpeedBooster in samus.itemList)), commName = "Above Charge Core"),
        Location(1, 10, 4, (S1 and samus.playerFlags["hasMissile"]), commName = "Crab Rave"),
        Location(1, 9, 6, (S1 and samus.playerFlags["hasMissile"]), bossAtLocation = Bosses.ChargeCoreX),
        Location(1, 12, 7, (S1 and (Item.SpeedBooster in samus.itemList) and (Item.Gravity in samus.itemList)), commName = "Watering Hole"),
        Location(1, 13, 8, S1, commName = "Crab Guardian"),
        Location(1, 1, 9, (S1 and (Item.ScrewAttack in samus.itemList) and (Item.WaveBeam in samus.itemList) and samus.playerFlags["hasMissile"]), bossAtLocation = Bosses.Ridley),
        Location(1, 3, 10, (S1 and (Item.ScrewAttack in samus.itemList) and (Item.DiffusionMissile in samus.itemList)), commName = "Tourian Ripper Maze"),
        Location(1, 8, 11, (S1 and (Item.ScrewAttack in samus.itemList) and (Item.PowerBomb in samus.itemList)), commName = "Animorphs")
        ]

    S2Locations = [Location(2, 5, 0, (samus.playerFlags["canEnterSectors"] and (Item.SpaceJump in samus.itemList) and (Item.ScrewAttack in samus.itemList)), commName = "Crumble City (Top)"),
        Location(2, 5, 1, (samus.playerFlags["canEnterSectors"] and (Item.SpaceJump in samus.itemList) and (Item.ScrewAttack in samus.itemList)), commName = "Crumble City (Bottom)"),
        Location(2, 4, 3, (samus.playerFlags["canEnterSectors"] and ((Item.HighJump in samus.itemList) or (Item.SpeedBooster in samus.itemList) or (Item.ScrewAttack in samus.itemList) or samus.playerFlags["canFreeze"])), commName = "Kago Jump"),
        Location(2, 9, 3, (S2 and (Item.Morph in samus.itemList) and samus.doorKey["blueDoors"]), commName = "Blue Locked Missiles"),
        Location(2, 1, 4, (samus.playerFlags["canEnterSectors"] and samus.doorKey["blueDoors"]), dataRoom = True),
        Location(2, 4, 4, (S2 and (Item.Morph in samus.itemList)), commName = "Before Data Room"),
        Location(2, 12, 4, (((Item.PowerBomb in samus.itemList) and samus.playerFlags["canEnterSectors"]) or (S2 and Item.SpaceJump)), commName = "Above Nettori"),
        Location(2, 0, 5, (S2 and samus.playerFlags["hasMissile"] and (Item.Morph in samus.itemList)), commName = "Below Data Room"),
        Location(2, 9, 5, (S2 and (Item.Morph in samus.itemList)), commName = "Zazabi Tower Exist"),
        Location(2, 13, 6, (samus.playerFlags["canEnterSectors"] and (Item.Morph in samus.itemList) and ((Item.PowerBomb in samus.itemList) or (Item.SpaceJump in samus.itemList) or (Item.ScrewAttack in samus.itemList)) and samus.playerFlags["hasBomb"] and samus.playerFlags["hasMissile"]), Bosses.Nettori),
        Location(2, 5, 8, (S2 and samus.playerFlags["canFreeze"] and (Item.Morph in samus.itemList)), commName = "Ripper Tower (Top)"),
        Location(2, 8, 8, (S2 and (Item.SpaceJump in samus.itemList)), commName = "Puyo Palace"),
        Location(2, 5, 10, (S2 and samus.playerFlags["canFreeze"] and (Item.Morph in samus.itemList)), commName = "Ripper Tower (Bottom)"),
        Location(2, 4, 11, (S2 and ((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList))), commName = "Oasis"),
        Location(2, 12, 11, (S2 and (Item.Morph in samus.itemList)), commName = "Zazabi E-Tank"),
        Location(2, 3, 12, (S2 and (Item.Morph in samus.itemList) and samus.playerFlags["canMorphJump"]), commName = "Wonderwall"),
        Location(2, 16, 12, (S2 and (Item.SpeedBooster in samus.itemList) and (Item.SpaceJump in samus.itemList) and (Item.ScrewAttack in samus.itemList) and samus.playerFlags["hasMissile"]), commName = "Zazabi Speedway (Top)"),
        Location(2, 14, 13, (S2 and samus.playerFlags["hasMissile"]), Bosses.Zazabi),
        Location(2, 2, 14, (S2 and (Item.Morph in samus.itemList) and samus.playerFlags["hasBomb"]), commName = "Blue Zorro Room"),
        Location(2, 16, 14, (S2 and (Item.SpeedBooster in samus.itemList) and (Item.ScrewAttack in samus.itemList) and samus.playerFlags["hasMissile"]), commName = "Zazabi Speedway (Bottom)")
        ]

    S3Locations = [Location(3, 15, 0, (S3 and (samus.doorKey["greenDoors"] or ((Item.ScrewAttack in samus.itemList) and (Item.SpeedBooster in samus.itemList) and ((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList))))), commName = "Top of Sector 3"),
        Location(3, 10, 1, (S3 and (samus.doorKey["greenDoors"] or ((Item.ScrewAttack in samus.itemList) and samus.playerFlags["hasBomb"])) and (Item.PowerBomb in samus.itemList)), commName = "Upper 3 PB-locked"),
        Location(3, 1, 2, (S3 and (Item.SpeedBooster in samus.itemList) and samus.playerFlags["hasBomb"] and (samus.playerFlags["hasBomb"] or (Item.WaveBeam in samus.itemList))), commName = "Speed Locked E"),
        Location(3, 11, 2, (S3 and (samus.doorKey["greenDoors"] or ((Item.ScrewAttack in samus.itemList) and ((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList)) and ((Item.WaveBeam in samus.itemList) or samus.playerFlags["hasBomb"])))), commName = "Upper 3 E-Tank"),
        Location(3, 18, 3, (S3 and samus.doorKey["greenDoors"]), dataRoom = True),
        Location(3, 20, 3, (S3 and samus.doorKey["greenDoors"] and (Item.ScrewAttack in samus.itemList) and (Item.SpeedBooster in samus.itemList) and ((Item.WaveBeam in samus.itemList) or (samus.playerFlags["canFreeze"] and ((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList))))), commName = "Garbage Chute (Upper)"),
        Location(3, 3, 4, (S3 and (Item.Varia in samus.itemList)), commName = "First H*ck Run"),
        Location(3, 11, 4, (S3 and (Item.SpeedBooster in samus.itemList) and (Item.Morph in samus.itemList) and (samus.playerFlags["hasBomb"] or (Item.ScrewAttack in samus.itemList))), commName = "BOB"),
        Location(3, 17, 4, (S3 and (samus.doorKey["greenDoors"])), commName = "Under Box"),
        Location(3, 0, 5, (S3 and (Item.SpeedBooster in samus.itemList) and (Item.ScrewAttack in samus.itemList) and samus.playerFlags["hasBomb"]), commName = "Porch"),
        Location(3, 6, 6, (S3 and (Item.SpeedBooster in samus.itemList)), commName = "Telltale Heart"),
        Location(3, 11, 6, (S3 and (Item.SpeedBooster in samus.itemList) and (Item.PowerBomb in samus.itemList)), commName = "PB Stretchy"),
        Location(3, 3, 8, (S3 and samus.doorKey["greenDoors"] and samus.playerFlags["canFreeze"]), bossAtLocation = Bosses.WideCoreX),
        Location(3, 18, 9, (S3 and samus.doorKey["greenDoors"] and samus.playerFlags["hasBomb"] and (samus.playerFlags["canFreeze"] or (Item.SpaceJump in samus.itemList)) and ((Item.WaveBeam in samus.itemList) or (samus.playerFlags["canFreeze"] and ((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList))))), commName = "Nova Stairs (Far)"),
        Location(3, 20, 9, (S3 and samus.doorKey["greenDoors"] and (Item.ScrewAttack in samus.itemList) and (Item.SpeedBooster in samus.itemList) and ((Item.WaveBeam in samus.itemList) or (samus.playerFlags["canFreeze"] and ((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList))))), commName = "Garbage Chute (Lower)"),
        Location(3, 14, 10, (S3 and samus.doorKey["greenDoors"]), commName = "Owtch Cushions"),
        Location(3, 17, 10, (S3 and samus.doorKey["greenDoors"] and samus.playerFlags["hasBomb"] and (samus.playerFlags["canFreeze"] or (Item.SpaceJump in samus.itemList)) and ((Item.WaveBeam in samus.itemList) or (samus.playerFlags["canFreeze"] and ((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList))))), commName = "Nova Stairs (Near)"),
        Location(3, 7, 11, (S3 and samus.doorKey["greenDoors"] and (Item.PowerBomb in samus.itemList) and (Item.Morph in samus.itemList)), commName = "Lava Maze")
        ]

    S4Locations = [Location(4, 10, 0, (S4 and samus.playerFlags["hasMissile"] and (Item.Morph in samus.itemList)), bossAtLocation = Bosses.Serris),
        Location(4, 13, 1, (S4  and samus.playerFlags["canMorphJump"] and samus.playerFlags["hasMissile"] and (Item.Morph in samus.itemList)), commName = "Serris Escape (Upper)"),
        Location(4, 9, 2, (S4), commName = "Broken Bridge"),
        Location(4, 14, 2, (S4  and samus.playerFlags["canMorphJump"] and (Item.Morph in samus.itemList)), commName = "Serris Escape (Lower)"),
        Location(4, 5, 3, (S4 and (Item.Morph in samus.itemList)), commName = "Owtch Room"),
        Location(4, 0, 6, (S4 and samus.doorKey["blueDoors"] and ((Item.SpeedBooster in samus.itemList) or (Item.Gravity in samus.itemList))), commName = "Pumpcon Trol"),
        Location(4, 9, 6, (S4 and (Item.SpeedBooster in samus.itemList) and (samus.doorKey["blueDoors"] or (Item.Gravity in samus.itemList))), commName = "Waterway"),
        Location(4, 12, 6, (samus.playerFlags["canEnterSectors"] and (Item.PowerBomb in samus.itemList)), commName = "PB Locked"),
        Location(4, 15, 6, (samus.playerFlags["canEnterSectors"] and ((Item.SuperMissile in samus.itemList) or (Item.WaveBeam in samus.itemList) or ((Item.Gravity in samus.itemList) and (Item.ScrewAttack in samus.itemList)))), commName = "Drain Pipe"),
        Location(4, 19, 6, (LS4 and samus.doorKey["redDoors"]), dataRoom = True),
        Location(4, 18, 7, (samus.playerFlags["canEnterSectors"] and (Item.Morph in samus.itemList) and ((Item.DiffusionMissile in samus.itemList) or ((Item.WaveBeam in samus.itemList) and (Item.IceBeam in samus.itemList)))), commName = "Upper-Lower 4"),
        Location(4, 19, 7, (samus.playerFlags["canEnterSectors"] and (Item.Morph in samus.itemList) and ((Item.DiffusionMissile in samus.itemList) or ((Item.WaveBeam in samus.itemList) and (Item.IceBeam in samus.itemList))) and (((Item.Gravity in samus.itemList) and (Item.ScrewAttack in samus.itemList)) or LS4)), commName = "Behind the Kago"),
        Location(4, 7, 8, (LS4 and (Item.Morph in samus.itemList)), commName = "Lower 4 Screw Blocks"),
        Location(4, 11, 8, (LS4), commName = "Worst Room in the Game"),
        Location(4, 7, 10, (LS4 and (Item.Morph in samus.itemList) and samus.playerFlags["hasMissile"] and (samus.playerFlags["hasBomb"] or (Item.ScrewAttack in samus.itemList))), commName = "Cheddar Bay"),
        Location(4, 10, 12, (LS4 and (Item.PowerBomb in samus.itemList)), commName = "The Thunderdome"),
        Location(4, 6, 14, (LS4 and (Item.Morph in samus.itemList) and ((Item.PowerBomb in samus.itemList) or (Item.WaveBeam in samus.itemList)) and samus.playerFlags["hasMissile"]), commName = "Crab Battle")
        ]

    S5Locations = [Location(5, 4, 1, (BS5 and (Item.SpeedBooster in samus.itemList)), commName = "Speed Trap (Rear)"),
        Location(5, 5, 1, (samus.playerFlags["canEnterSectors"] and (((Item.Morph in samus.itemList) and samus.playerFlags["hasMissile"]) or samus.doorKey["yellowDoors"])), commName = "Speed Trap (Front)"),
        Location(5, 11, 1, (BS5 and samus.playerFlags["hasBomb"] and (Item.Morph in samus.itemList)), commName = "Crow's Nest"),
        Location(5, 3, 4, (samus.playerFlags["canEnterSectors"] and samus.doorKey["yellowDoors"]), commName = "Magic Box"),
        Location(5, 5, 4, (samus.playerFlags["canEnterSectors"] and samus.doorKey["yellowDoors"] and (Item.Morph in samus.itemList) and samus.playerFlags["hasBomb"]), commName = "Mama Gerubus"),
        Location(5, 18, 4, (BS5 and (Item.PowerBomb in samus.itemList) and (Item.Morph in samus.itemList)), commName = "Nightmare Recharge"),
        #Edge case, not technically a boss item however to reach this item, players will have to fight
        #Nightmare. Need a way of taking into account player damage output before randoing this location
        #Maybe set bossAtLocation to Nightmare and then just hardcode "If bossAtLocation = True and Location = S5-22-4,
        # in spoiler log, just output location like normal?" Idk, a problem for the future
        Location(5, 22, 4, (BS5 and (Item.Morph in samus.itemList) and samus.playerFlags["hasBomb"]), commName = "Above Nightmare"),
        Location(5, 6, 5, (S5 and (Item.Morph in samus.itemList) and samus.playerFlags["canFreeze"]), commName = "Ripper Road"),
        Location(5, 12, 5, (S5 and samus.doorKey["yellowDoors"]), dataRoom = True),
        Location(5, 17, 5, (BS5 and (Item.Morph in samus.itemList) and samus.playerFlags["hasBomb"]), commName = "Break Room"),
        Location(5, 22, 6, (BS5), bossAtLocation = Bosses.Nightmare),
        Location(5, 8, 7, (S5 and (Item.PowerBomb in samus.itemList) and ((Item.SpaceJump in samus.itemList) or samus.playerFlags["canFreeze"])), commName = "Above Yellow Locks"),
        Location(5, 12, 7, (S5 and samus.doorKey["yellowDoors"] and (samus.playerFlags["canFreeze"] or (Item.SpaceJump in samus.itemList))), commName = "Fake E-Tank"),
        Location(5, 15, 7, (BS5 and (Item.Varia in samus.itemList) and samus.playerFlags["hasMissile"] and samus.playerFlags["canMorphJump"] and (Item.Morph in samus.itemList)), commName = "Mini Fridge"),
        Location(5, 20, 7, (BS5 and (Item.SpeedBooster in samus.itemList) and (Item.Gravity in samus.itemList)), commName = "Airlock"),
        Location(5, 14, 8, (S5 and (Item.Morph in samus.itemList) and ((Item.SpaceJump in samus.itemList) or samus.playerFlags["canFreeze"]) and samus.doorKey["yellowDoors"]), commName = "200 Missile"),
        Location(5, 7, 11, (S5 and (Item.PowerBomb in samus.itemList)), commName = "Bottom of Lower 5")
        ]

    S6Locations = [Location(6, 5, 3, (samus.playerFlags["canEnterSectors"] and (Item.Morph in samus.itemList) and ((Item.SpeedBooster in samus.itemList) or samus.playerFlags["hasBomb"])), commName = "Sector 6 First Item"),
        Location(6, 8, 3, (samus.playerFlags["canEnterSectors"] and (Item.Morph in samus.itemList) and ((Item.SuperMissile in samus.itemList) or (Item.SpeedBooster in samus.itemList) or (Item.ScrewAttack in samus.itemList)) and samus.playerFlags["hasBomb"]), commName = "Mission Impossible"),
        Location(6, 14, 3, (S6 and samus.playerFlags["hasBomb"] and (Item.Morph in samus.itemList)), commName = "Fake Missile Tank"),
        Location(6, 3, 4, (S6 and samus.doorKey["redDoors"] and (Item.ScrewAttack in samus.itemList) and (Item.PowerBomb in samus.itemList) and (Item.SpeedBooster in samus.itemList)), commName = "Space Boost Alley (Upper)"),
        Location(6, 14, 4, (S6 and (Item.ScrewAttack in samus.itemList) and (Item.SpeedBooster in samus.itemList) and (Item.Bombs in samus.itemList)), commName = "Pillar Highway"),
        Location(6, 9, 5, (S6 and samus.doorKey["redDoors"] and (Item.Morph in samus.itemList) and (Item.PowerBomb in samus.itemList)), commName = "Run Crumbler"),
        Location(6, 1, 6, (S6 and samus.doorKey["redDoors"] and (Item.ScrewAttack in samus.itemList) and (Item.SpeedBooster in samus.itemList) and (Item.PowerBomb in samus.itemList) and (Item.SpaceJump in samus.itemList)), commName = "Space Boost Alley (Lower)"),
        Location(6, 7, 6, (S6 and samus.doorKey["redDoors"] and (Item.PowerBomb in samus.itemList)), bossAtLocation = Bosses.BoxTwo),
        Location(6, 10, 6, (S6 and samus.doorKey["redDoors"] and (Item.PowerBomb in samus.itemList) and (Item.WaveBeam in samus.itemList)), commName = "XBOX Garage"),
        Location(6, 6, 8, (S6 and (Item.SpeedBooster in samus.itemList)), commName = "Free E-Tank"),
        Location(6, 12, 8, (S6 and (((Item.ScrewAttack in samus.itemList) and samus.playerFlags["hasBomb"]) or ((Item.SpeedBooster in samus.itemList) and (Item.PowerBomb in samus.itemList) and samus.doorKey["greenDoors"]))), commName = "Pantry"),
        Location(6, 11, 9, (S6 and (Item.Morph in samus.itemList) and (((Item.ScrewAttack in samus.itemList) and samus.playerFlags["hasBomb"]) or ((Item.SpeedBooster in samus.itemList) and (Item.PowerBomb in samus.itemList) and samus.doorKey["greenDoors"])) and (((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList)) or samus.playerFlags["canFreeze"])), commName = "Higher Jump Hole"),
        Location(6, 5, 11, (S6 and (Item.SpeedBooster in samus.itemList) and (Item.PowerBomb in samus.itemList) and (Item.Morph in samus.itemList) and (((Item.HighJump in samus.itemList) or (Item.SpaceJump in samus.itemList)) or samus.playerFlags["canFreeze"])), commName = "Wine Cellar"),
        Location(6, 11, 11, (S6 and (Item.SpeedBooster in samus.itemList) and (Item.ChargeBeam in samus.itemList) and (Item.Morph in samus.itemList) and (Item.PowerBomb in samus.itemList) and samus.playerFlags["hasMissile"] and samus.doorKey["greenDoors"]), bossAtLocation = Bosses.ChargeCoreX)
        ]

    allSectors = [
        Sector(missileFirstPath, True),
        Sector(mainDeckLocations, True),
        Sector(S1Locations, True),
        Sector(S2Locations, True),
        Sector(S3Locations, samus.doorKey["blueDoors"]),
        Sector(S4Locations, samus.doorKey["blueDoors"]),
        Sector(S5Locations, samus.doorKey["greenDoors"]),
        Sector(S6Locations, samus.doorKey["greenDoors"])
    ]
          

def initRando(majMinItemSplit, missileUpgradesEnableMissiles, bombsEnablePB, damageRuns, splitSecurityLevels, sectorShuffle, showCommNames, difficulty):
    global randomizer
    randomizer = Rando(majMinItemSplit, missileUpgradesEnableMissiles, bombsEnablePB, damageRuns, splitSecurityLevels, sectorShuffle, showCommNames, difficulty)
    main()

class Location:
    
    def __init__(self, sector, X, Y, itemRequirements, bossAtLocation = None, dataRoom = False, itemAtLocation = None, commName = ""):
        self.sector = sector
        self.X = X
        self.Y = Y
        self.itemRequirements = itemRequirements
        self.itemAtLocation = itemAtLocation
        self.bossAtLocation = bossAtLocation
        self.dataRoom = dataRoom
        self.commName = commName

    def set_item(self, newItem):
        self.itemAtLocation = newItem

    def __str__(self):
        return "S" + str(self.sector) + "-" + str(self.X) + "-" + str(self.Y)

    def __eq__(self, toCompare):
        if self.sector == toCompare.sector and self.X == toCompare.X and self.Y == toCompare.Y:
            return True
        else:
            return False

class Player:

    def __init__(self):
        self.itemList = []
        self.health = 99
        self.missileDamage = 0
        
        self.playerFlags = {
            #player can have any item in flagKey entry to be True
            "hasMissile":(Item.Missile in self.itemList) or (Item.SuperMissile in self.itemList) or (Item.IceMissile in self.itemList) or (Item.DiffusionMissile in self.itemList),
            "hasBomb":(Item.Morph in self.itemList) and ((Item.Bombs in self.itemList) or (Item.PowerBomb in self.itemList)),
            "canFreeze":(Item.IceMissile in self.itemList) or (Item.IceBeam in self.itemList),
            "canMorphJump":((Item.Bombs in self.itemList) or (Item.HighJump in self.itemList)) and Item.Morph in self.itemList,
            "canEnterSectors":(Item.SpeedBooster in self.itemList) or (Item.Morph in self.itemList)}
        
        self.doorKey = {
            "blueDoors":self.playerFlags["canEnterSectors"],
            "greenDoors": self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and self.playerFlags["hasBomb"] and self.playerFlags["canMorphJump"],
            "yellowDoors":self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and self.playerFlags["hasBomb"] and (Item.Varia in self.itemList),
            "redDoors":self.playerFlags["canEnterSectors"] and (Item.SpeedBooster in self.itemList) and (Item.Gravity in self.itemList) and (self.playerFlags["hasBomb"] or (Item.ScrewAttack in self.itemList))}
    

    def addItem(self, item):
        self.itemList.append(item)
        
        self.playerFlags = {
            #player can have any item in flagKey entry to be True
            "hasMissile":(Item.Missile in self.itemList) or (Item.SuperMissile in self.itemList) or (Item.IceMissile in self.itemList) or (Item.DiffusionMissile in self.itemList),
            "hasBomb":(Item.Morph in self.itemList) and ((Item.Bombs in self.itemList) or (Item.PowerBomb in self.itemList)),
            "canFreeze":(Item.IceMissile in self.itemList) or (Item.IceBeam in self.itemList),
            "canMorphJump":(Item.Bombs in self.itemList) or (Item.HighJump in self.itemList),
            "canEnterSectors":(Item.SpeedBooster in self.itemList) or (Item.Morph in self.itemList)}

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
     
        self.playerFlags = {
            #player can have any item in flagKey entry to be True
            "hasMissile":(Item.Missile in self.itemList) or (Item.SuperMissile in self.itemList) or (Item.IceMissile in self.itemList) or (Item.DiffusionMissile in self.itemList),
            "hasBomb":(Item.Morph in self.itemList) and ((Item.Bombs in self.itemList) or (Item.PowerBomb in self.itemList)),
            "canFreeze":(Item.IceMissile in self.itemList) or (Item.IceBeam in self.itemList),
            "canMorphJump":(Item.Bombs in self.itemList) or (Item.HighJump in self.itemList),
            "canEnterSectors":(Item.SpeedBooster in self.itemList) or (Item.Morph in self.itemList)}

    def giveETank(self):
        self.health = self.health + 100

    def getHealth(self):
        return str(self.health)

class Rando():
    
    def __init__(self, majMinItemSplit, missileUpgradesEnableMissiles, bombsEnablePB, damageRuns, splitSecurityLevels, sectorShuffle, showCommNames, difficulty):
        self.majMinItemSplit = majMinItemSplit
        self.missileUpgradesEnableMissiles = missileUpgradesEnableMissiles
        self.bombsEnablePB = bombsEnablePB
        self.damageRuns = damageRuns
        self.splitSecurityLevels = splitSecurityLevels
        self.sectorShuffle = sectorShuffle
        self.showCommNames = showCommNames
        self.difficulty = difficulty

class Boss():
    #Health is self explanitory
    #itemToLeave as in, the item(s) required to leave the bosses location
    #(i.e. SpaceJump is hard required to leave Yakuza's arena)
    def __init__(self, health, itemToLeave):
        self.health = health
        self.itemToLeave = itemToLeave

class Sector():
    def __init__(self, itemLocations, doorReq):
        self.itemLocations = itemLocations
        self.doorReq = doorReq

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
    '''
    BoxOne is ommitted because you don't actually expose its CoreX until XBox
    MegaCore and WideCore have 0 health because, even though they do have health
    requirements, there are none to consider as far as the rando is concerned because
    the rando will only check to make sure the player has enough missiles before requiring
    a boss. I could probably add samus.playerFlags["hasMissile"] in there as a requirment so
    your first missile requirement isn't on either of those bosses but ¯\_(ツ)_/¯ I'm sure
    it'll be fine
    '''
    Arachnus = Boss(150, [Item.Morph])
    ChargeCoreX = Boss(33, [Item.ChargeBeam])
    Zazabi = Boss(100, [Item.HighJump, Item.SpaceJump, Item.ChargeBeam])
    Serris = Boss(50, [Item.SpeedBooster, Item.ChargeBeam])
    MegaCoreX = Boss(0, [Item.ChargeBeam])
    WideCoreX = Boss(0, [Item.ChargeBeam, Item.Varia])
    Yakuza = Boss(1000, [Item.SpaceJump, Item.ChargeBeam])
    Nettori = Boss(2000, [Item.ChargeBeam])
    Nightmare = Boss(1200, [Item.SpeedBooster, Item.Gravity, Item.ChargeBeam])
    BoxTwo = Boss(500, [Item.WaveBeam, Item.ScrewAttack, Item.ChargeBeam])
    Ridley = Boss(4500, [Item.SpaceJump, Item.ChargeBeam])
    


if __name__ == "__main__":
    main()
