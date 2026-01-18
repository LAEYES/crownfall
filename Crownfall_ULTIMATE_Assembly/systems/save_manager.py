
import json, os

class SaveManager:
    def __init__(self):
        os.makedirs("saves", exist_ok=True)

    def save(self, world, slot=1):
        with open(f"saves/save_{slot}.json", "w") as f:
            json.dump({
                "economy": world.economy.market,
                "factions": [(f.name, f.relation, f.gold) for f in world.factions]
            }, f)

    def load(self, world, slot=1):
        try:
            with open(f"saves/save_{slot}.json") as f:
                data = json.load(f)
            world.economy.market = data["economy"]
            for f, d in zip(world.factions, data["factions"]):
                f.name, f.relation, f.gold = d
        except:
            pass
