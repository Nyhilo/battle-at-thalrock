from operator import attrgetter
from roll import roll, roll_no_min

import weapon
from log import log

class MobType:
    Soldier = "Soldier"
    Archer = "Archer"
    Commander = "Commander"

class Faction:
    Dwarf = "Dwarf"
    Human = "Human"

class Mob:
    def __init__(self, name: str, mobType: MobType, faction: Faction, hp: int = 0, ac: int = 0, strength: int = 0,
        dex: int = 0, bab: int = 0, meleeAtkBonus: int = 0, weapons = None):
        self.alive = True

        self.name = name
        self.type = mobType
        self.faction = faction

        self.factionColor = "blue" if self.faction == Faction.Dwarf else "red"

        self.HP = hp
        self.AC = ac
        self.strength = strength
        self.dex = dex
        self.bab = bab
        self.meleeAtkBonus = meleeAtkBonus
        self.weapons = weapons

        # If only a single weapon was given
        if not isinstance(weapons, list):
            self.weapons = [weapons]

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return (
            "Name: " + self.name + "\n"
            "HP: " + str(self.HP) + "\n"
            "AC: " + str(self.AC) + "\n"
            "Str: " + str(self.strength) + "\n"
            "Dex: " + str(self.dex) + "\n"
            "Bab: " + str(self.bab) + "\n"
            "mBonus: " + str(self.meleeAtkBonus) + "\n"
            "weapons: " + ", ".join([w.__repr__() for w in self.weapons]) + "\n"
        )


    def hurt(self, amount):
        self.HP -= amount
        self.alive = self.HP > 0


    def heal(self, amount):
        self.hurt(-amount)


    def attack(self, enemy, weaponType: int = weapon.Type.Melee):
        if len(self.weapons) == 0:
            enemy.hurt(1)
        
        # You need a ranged weapon to make a ranged attack
        if (weaponType == weapon.Type.Ranged
                and not any(w.Ranged for w in self.weapons)):
            log(f"{self.name} couldn't hit {enemy.name} because they don't have a ranged weapon!",
                2, color=self.factionColor, attrs=["dark"])
            return enemy
        
        # Determine what weapon should be used
        myWeapon = max(self.weapons, key=attrgetter("damage"))
        
        # Prioritize weapons that match the given type, if available
        typedWeapons = list(filter(lambda w: w.type == weaponType, self.weapons))
        if (len(typedWeapons) != 0):
            myWeapon = max(typedWeapons, key=attrgetter("damage"))

        # Calculate hit
        if myWeapon:
            atkBonus = self.bab + (self.strength if myWeapon.type == weapon.Type.Melee else self.dex)

            # Miss?
            atkRoll = roll(20)
            if atkRoll + atkBonus < enemy.AC:
                a = "an" if myWeapon.name[0] in 'aeiouAEIOU' else "a"
                log(f"{self.name} tried to hit {enemy.name} with {a} {myWeapon.name}, but missed!",
                    2, color=self.factionColor, attrs=["dark"])
                return enemy
            
            crit = atkRoll >= myWeapon.critThreshold
            critMult = myWeapon.critMultiplier if crit else 1

            damage = (roll(myWeapon.damage) + self.strength) * critMult
            enemy.hurt(damage)

            hit = "hit" if enemy.alive else "killed"
            critmsg = " Critical hit!" if crit else ""
            critdelay = 4 if crit else 2 if not enemy.alive else 1
            textAttributes = []
            if crit:
                textAttributes.append("bold")
            if enemy.alive:
                textAttributes.append("dark")
        
            log(f"{self.name} {hit} {enemy.name} with a {myWeapon.name} for {damage} damage!{critmsg}",
                2, critdelay, color=self.factionColor, attrs=textAttributes)

            return enemy


class DwarfSoldier(Mob):
    def __init__(self):
        super().__init__(
            name="Dwarf Soldier",
            mobType=MobType.Soldier,
            faction=Faction.Dwarf,
            hp=roll(10) + 3,
            ac=15,
            strength=1,
            dex=2,
            bab=1,
            meleeAtkBonus=1,
            weapons=weapon.Axe()
        )


class DwarfCommander(Mob):
    def __init__(self):
        super().__init__(
            name="Dwarf Commander",
            mobType=MobType.Commander,
            faction=Faction.Dwarf,
            hp=roll_no_min(10) + 3,
            ac=16,
            strength=1,
            dex=2,
            bab=2,
            meleeAtkBonus=1,
            weapons=weapon.Axe()
        )


class DwarfArcher(Mob):
    def __init__(self):
        super().__init__(
            name="Dwarf Archer",
            mobType=MobType.Archer,
            faction=Faction.Dwarf,
            hp=roll(10) + 3,
            ac=15,
            strength=1,
            dex=2,
            bab=1,
            meleeAtkBonus=1,
            weapons=[weapon.Shortbow()]
        )


class HumanSoldier(Mob):
    def __init__(self):
        super().__init__(
            name="Human Soldier",
            mobType=MobType.Soldier,
            faction=Faction.Human,
            hp=roll(10) + 3,
            ac=17,
            strength=2,
            dex=1,
            bab=1,
            weapons=weapon.Longspear()
        )

    
class HumanCommander(Mob):
    def __init__(self):
        super().__init__(
            name="Human Commander",
            mobType=MobType.Commander,
            faction=Faction.Human,
            hp=roll_no_min(10) + 3,
            ac=17,
            strength=2,
            dex=1,
            bab=1,
            weapons=weapon.Greatsword()
        )


class HumanArcher(Mob):
    def __init__(self):
        super().__init__(
            name="Human Archer",
            mobType=MobType.Archer,
            faction=Faction.Human,
            hp=roll(10) + 3,
            ac=17,
            strength=2,
            dex=1,
            bab=1,
            weapons=[weapon.Longbow()]
        )
