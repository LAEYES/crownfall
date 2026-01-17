
class Chronicle:
    def __init__(self):
        self.entries = []

    def add(self, text):
        self.entries.append(text)

    def log_turn(self, kingdom):
        self.entries.append(
            f"Week ends with population {kingdom.population} and morale {kingdom.morale}."
        )

    def print(self):
        for e in self.entries:
            print("-", e)
