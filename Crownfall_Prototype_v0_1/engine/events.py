
def check_events(kingdom, chronicle):
    if kingdom.food < 20:
        kingdom.morale -= 5
        chronicle.add("Famine spreads across the land.")

    if kingdom.morale < 30:
        kingdom.loyalty -= 5
        chronicle.add("The people whisper of rebellion.")

    if kingdom.loyalty < 20:
        kingdom.fear += 5
        chronicle.add("Authority is enforced by fear.")
