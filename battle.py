from functools import reduce

import field
import mob
from roll import set_seed, roll
import log


def get_dwarf_win_state(battlefield):
    # Enemy human units
    units = list(filter(lambda u: u.faction == field.Faction.Human, battlefield.units))

    # Humans retreat when their numbers fall below 30%
    enemyFighters = reduce(list.__add__, [unit.fighters for unit in units])
    totalEnemyFighters = len(enemyFighters)
    livingEnemyFighters = list(filter(lambda f: f.alive, enemyFighters))
    totalLivingEnemyFighters = len(livingEnemyFighters)

    if totalEnemyFighters == 0:
        return (True, "The enemy has been wiped out entirely")

    if totalLivingEnemyFighters / totalEnemyFighters < .3:
        return (True, "The enemy has retreated!")

    return (False, None)

# Use this function if it is decided that the humans will not retreat
def get_dwarf_total_war_win_state(battlefield):
    # Enemy human units
    units = list(filter(lambda u: u.faction == field.Faction.Human, battlefield.units))

    # The humans will fight to the death for their king
    enemyFighters = reduce(list.__add__, [unit.fighters for unit in units])
    livingEnemyFighters = list(filter(lambda f: f.alive, enemyFighters))
    totalLivingEnemyFighters = len(livingEnemyFighters)

    if totalLivingEnemyFighters == 0:
        return (True, "The enemy has been wiped out entirely")

    return (False, None)


def get_human_win_state(battlefield):
    # Enemy dwarf units
    units = list(filter(lambda u: u.faction == field.Faction.Dwarf, battlefield.units))

    # Dwarfs fight for their home to the death
    enemyFighters = reduce(list.__add__, [unit.fighters for unit in units])
    livingEnemyFighters = list(filter(lambda f: f.alive, enemyFighters))
    totalLivingEnemyFighters = len(livingEnemyFighters)

    if totalLivingEnemyFighters == 0:
        return (True, "All of our allies have fallen in this battle.")

    return (False, None)


def log_remaining(battlefield, side: field.Faction):

        soldiers = list(filter(lambda u:
                                    u.faction == side and
                                    u.type == field.UnitType.Soldier, battlefield.units))[0]
        archers = list(filter(lambda u:
                                    u.faction == side and
                                    u.type == field.UnitType.Archer, battlefield.units))[0]
        commanders = list(filter(lambda u:
                                    u.faction == side and
                                    u.type == field.UnitType.Commander, battlefield.units))[0]

        color = "blue" if side == field.Faction.Dwarf else "Red"

        log.log(f"\nThose who are left: {side}", color=color, attrs=["underline"])
        log.log(f"Soldiers: {soldiers.living_count()}", 1, color=color)
        log.log(f"Archers: {archers.living_count()}", 1, color=color)
        log.log(f"Commanders: {commanders.living_count()}", 1, color=color)
        log.log("", sleepMultiplier=4, color=color)


def Battle(battlefield):
    log.log(battlefield.name, sleepMultiplier=4, color="white", colorBackground="on_grey", attrs=["underline"])

    roundCounter = 0
    dwarfWinReason = None
    humanWinReason = None
    dwarfWin = False
    humanWin = False
    while not dwarfWin and not humanWin:
        roundCounter += 1
        log.log(f"Round {roundCounter}", 1, 3, attrs=["bold"])
        for i in range(len(battlefield.units)):
            currentUnit = battlefield.units[i]
            living = currentUnit.living_count()

            if living > 0:
                s = "s" if living > 1 else ""
                have = "have" if living > 1 else "has"
                log.log(f"{living} {currentUnit}{s} {have} an initiative of {currentUnit.initiative}",
                    2, 3, attrs=["underline"])

                battlefield.skirmish(i)

                log.log("", 0 , 1)

        humanWin, humanWinReason = get_human_win_state(battlefield)
        dwarfWin, dwarfWinReason = get_dwarf_win_state(battlefield)
        # dwarfWin, dwarfWinReason = get_dwarf_total_war_win_state(battlefield)


    log.log(f"\nResult of combat on the {battlefield.name}", sleepMultiplier=6, newline=False, attrs=["underline"])
    log.log(".", sleepMultiplier=6, newline=False)
    log.log(".", sleepMultiplier=6, newline=False)
    log.log(".", sleepMultiplier=6)

    if dwarfWin and humanWin:
        log.log(dwarfWinReason, 1, 1, color="blue")
        log.log("but...", 1)
        log.log(humanWinReason, 1, 3, color="red")
        log_remaining(battlefield, field.Faction.Dwarf)
        log_remaining(battlefield, field.Faction.Human)

        return

    if dwarfWin:
        log.log(dwarfWinReason, 1, 2, color="blue")
        log.log("The dwarves are victorious!", 1, 4, color="blue", attrs=["bold"])
        log_remaining(battlefield, field.Faction.Dwarf)

    if humanWin:
        log.log(humanWinReason, 1, 3, color="red")
        log.log("The humans are headed toward the city!", 1, 4, color="red", attrs=["bold"])
        log_remaining(battlefield, field.Faction.Human)

    log.log("\n", sleepMultiplier=2)
        



if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1:
        set_seed(argv[1])

    if len(argv) > 2:
        log._sleepTime_ = float(argv[2])

    westBattleField = field.Battlefield("West BattleField",
                                         9, 8, 3, 1,
                                        12, 2, 1, 1)

    eastBattleField = field.Battlefield("East BattleField",
                                        12, 10, 4, 1,
                                        15,  3, 1, 1)
    
    log.log("", sleepMultiplier=3)
    log.log("The humans have orders to retreat if their numbers drop below 30%.", sleepMultiplier=8, color="red")
    log.log("The dwarves are protecting their home, and are willing to fight to the death.\n", sleepMultiplier=8, color="blue")

    Battle(westBattleField)
    
    Battle(eastBattleField)



