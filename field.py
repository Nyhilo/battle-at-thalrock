from typing import List
from random import shuffle

import mob
import weapon
from roll import roll
from log import log

DEBUG = False

def debug(msg):
    if DEBUG:
        print(f"Debug: {msg}")


class UnitType:
    Soldier = "Soldier"
    Archer = "Archer"
    Commander = "Commander"

class Faction:
    Dwarf = "Dwarf"
    Human = "Human"

class Unit:
    def __init__(self, fighters: List[mob.Mob], unitType, faction, initiative):
        self.fighters = fighters
        self.type = unitType
        self.faction = faction
        self.initiative = roll(20) + initiative


    def __str__(self):
        return self.faction + " " + self.type


    def living_count(self):
        living = list(filter(lambda f: f.alive, self.fighters))
        return len(living)


class Battlefield:
    def __init__(self, name,
                       dwarfSoldiers, dwarfArchers, dwarfCommanders, dwarfInitiativeBonus,
                       humanSoldiers, humanArchers, humanCommanders, humanInitiativeBonus):

        self.name = name

        # Populate each side of the conflict
        unosrtedUnits = [
            Unit([mob.DwarfSoldier() for _ in range(dwarfSoldiers)], UnitType.Soldier, Faction.Dwarf, dwarfInitiativeBonus),
            Unit([mob.DwarfArcher() for _ in range(dwarfArchers)], UnitType.Archer, Faction.Dwarf, dwarfInitiativeBonus),
            Unit([mob.DwarfCommander() for _ in range(dwarfCommanders)], UnitType.Commander, Faction.Dwarf, dwarfInitiativeBonus),

            Unit([mob.HumanSoldier() for _ in range(humanSoldiers)], UnitType.Soldier, Faction.Human, humanInitiativeBonus),
            Unit([mob.HumanArcher() for _ in range(humanArchers)], UnitType.Archer, Faction.Human, humanInitiativeBonus),
            Unit([mob.HumanCommander() for _ in range(humanCommanders)], UnitType.Commander, Faction.Human, humanInitiativeBonus)
        ]

        # Sort by initiative order
        self.units = sorted(unosrtedUnits, key=lambda u: u.initiative, reverse=True)


    # Tracks the index of the unit with the current initiative
    currentInitiative = 0
    
    def get_enemy_indicies(self, enemyFaction):
        return list(
                filter(
                    lambda i: self.units[i].faction == enemyFaction and self.units[i].living_count() > 0,
                    range(len(self.units))))


    def get_target_index_by_target_type_priority(self, unitIndicies, priorityList) -> int:
        for typePriority in priorityList:
            for index in unitIndicies:
                if self.units[index].type == typePriority:
                    return index

        return None


    def attack_first(self, attacker, enemyUnitIndex):
        # Loop through the fighters in the target unit until we find one that's still alive
        for enemyIndex in range(len(self.units[enemyUnitIndex].fighters)):
            if self.units[enemyUnitIndex].fighters[enemyIndex].alive:
                debug(f"Fighter identified for attack: {self.units[enemyUnitIndex].fighters[enemyIndex].name}")

                attacker.attack(self.units[enemyUnitIndex].fighters[enemyIndex])
                return # Return after the first enemy is attacked in the unit

        log(attacker + " could not find an enemy to attack in the target unit.", 2)


    def target(self, attacker, enemyIndicies):
        targetPriority = [UnitType.Soldier, UnitType.Commander, UnitType.Archer]

        # Archers have a chance for a random priority
        if attacker.type == UnitType.Archer and roll(20) > 15:
            shuffle(targetPriority)

        enemyUnitIndex = self.get_target_index_by_target_type_priority(
            enemyIndicies,
            targetPriority)

        debug(f"Index of target: {enemyUnitIndex}")

        if enemyUnitIndex != None:
            self.attack_first(attacker, enemyUnitIndex)


    def skirmish(self, attackerIndex):
        # Can't fight if we have no one to fight with
        if self.units[attackerIndex].living_count() == 0:
            return

        # Determine which units are part of this fight
        attackerFaction = self.units[attackerIndex].faction
        enemyFaction = Faction.Human if attackerFaction == Faction.Dwarf else Faction.Dwarf
        
        for fighter in list(filter(lambda f: f.alive, self.units[attackerIndex].fighters)):
            # Get enemy units that still have active fighters
            enemyIndices = self.get_enemy_indicies(enemyFaction)
            
            debug(enemyIndices)
            
            if len(enemyIndices) == 0:
                return

            self.target(fighter, enemyIndices)

