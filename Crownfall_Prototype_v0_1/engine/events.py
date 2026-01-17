
import random


def check_events(kingdom, chronicle, season):
    if kingdom.food < 20:
        kingdom.morale -= 5
        chronicle.add("Famine spreads across the land.")

    if kingdom.morale < 30:
        kingdom.loyalty -= 5
        chronicle.add("The people whisper of rebellion.")

    if kingdom.loyalty < 20:
        kingdom.fear += 5
        chronicle.add("Authority is enforced by fear.")

    if kingdom.unrest > 50 and random.random() < 0.2:
        kingdom.gold = max(0, kingdom.gold - 10)
        kingdom.stability -= 4
        chronicle.add("Civil unrest disrupts tax collection.")

    if season == "Winter" and random.random() < 0.2:
        kingdom.morale -= 3
        chronicle.add("Blizzards disrupt trade and morale.")

    if random.random() < 0.15:
        caravan_gold = random.randint(8, 18)
        kingdom.gold += caravan_gold
        chronicle.add(f"A trade caravan arrives with {caravan_gold} gold.")

    if random.random() < 0.12:
        kingdom.food += 12
        chronicle.add("A bountiful harvest fills the granaries.")

    if random.random() < 0.08:
        loss = min(kingdom.population, 3)
        kingdom.population -= loss
        kingdom.morale -= 4
        chronicle.add("A plague claims lives in the capital.")

    if random.random() < 0.1 and kingdom.army > 0:
        kingdom.army -= 1
        kingdom.morale += 2
        chronicle.add("The army drills in the countryside, boosting morale.")

    if random.random() < 0.1 and kingdom.infrastructure > 1:
        kingdom.infrastructure += 1
        chronicle.add("Artisans improve infrastructure with clever designs.")

    if random.random() < 0.08 and kingdom.housing > 0:
        kingdom.population += 2
        chronicle.add("Settlers arrive seeking new homes in the kingdom.")
