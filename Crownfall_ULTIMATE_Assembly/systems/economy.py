
class EconomySystem:
    def __init__(self):
        self.market = {
            "food": {"supply": 100, "demand": 80, "price": 1.0},
            "iron": {"supply": 50, "demand": 60, "price": 2.5}
        }

    def update(self, dt):
        for r in self.market.values():
            delta = r["demand"] - r["supply"]
            r["price"] += delta * 0.0005
            r["price"] = max(0.1, r["price"])
