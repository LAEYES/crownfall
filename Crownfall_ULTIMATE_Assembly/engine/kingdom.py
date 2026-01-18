
class Kingdom:
    def __init__(self):
        self.gold=50
        self.food=80
        self.population=40
        self.morale=60
        self.loyalty=60
        self.fear=20
        self.collapsed=False

    def produce(self):
        self.food+=2
        self.gold+=1

    def consume(self):
        self.food-=self.population*0.2
        if self.food<0:
            self.morale-=5
