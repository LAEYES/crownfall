
def check_events(kingdom,chronicle):
    if kingdom.food<20:
        kingdom.morale-=2
        chronicle.add("Famine spreads across the land.")
