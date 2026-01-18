
class StrategicAI:
    def __init__(self, factions):
        self.factions = factions

    def update(self, dt):
        for f in self.factions:
            if not f.playable:
                if f.gold < 50:
                    f.state = "trade"
                    f.gold += 1
                else:
                    f.state = "war"
