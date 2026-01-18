
class Chronicle:
    def __init__(self):
        self.entries = []
        self.current_turn = []

    def start_turn(self):
        self.current_turn = []

    def add(self, text):
        self.entries.append(text)
        self.current_turn.append(text)

    def log_turn(self, kingdom):
        summary = (
            f"Week ends with population {kingdom.population} and morale {kingdom.morale}."
        )
        self.entries.append(summary)
        self.current_turn.append(summary)

    def print(self):
        for e in self.entries:
            print("-", e)

    def last_turn_entries(self):
        return list(self.current_turn)
