
class Kingdom:
    def __init__(self):
        self.gold = 50
        self.food = 80
        self.population = 40
        self.morale = 60
        self.loyalty = 60
        self.fear = 20
        self.collapsed = False

    def produce(self):
        self.food += 10
        self.gold += 5

    def consume(self):
        self.food -= self.population * 0.8
        if self.food < 0:
            self.morale -= 10
            self.population -= 2
        if self.morale <= 0 or self.population <= 0:
            self.collapsed = True

    def display(self):
        print(f"Pop:{self.population} Food:{int(self.food)} Gold:{self.gold} Morale:{self.morale}")
