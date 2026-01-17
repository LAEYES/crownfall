
class Kingdom:
    def __init__(self):
        self.gold = 50
        self.food = 80
        self.population = 40
        self.morale = 60
        self.loyalty = 60
        self.fear = 20
        self.infrastructure = 1
        self.farms = 1
        self.mines = 1
        self.army = 5
        self.tax_rate = 1.0
        self.collapsed = False

    def produce(self, season):
        season_food_bonus = {
            "Spring": 1.2,
            "Summer": 1.1,
            "Autumn": 1.0,
            "Winter": 0.7,
        }
        morale_factor = max(self.morale, 10) / 100
        infra_factor = 1 + (self.infrastructure * 0.08)
        food_gain = 8 * self.farms * infra_factor * season_food_bonus.get(season, 1.0)
        gold_gain = 4 * self.mines * infra_factor * self.tax_rate
        self.food += food_gain * morale_factor
        self.gold += int(gold_gain * morale_factor)

    def consume(self, season):
        season_food_need = {"Winter": 1.1}
        self.food -= self.population * 0.7 * season_food_need.get(season, 1.0)
        if self.tax_rate > 1.2:
            self.morale -= 2
            self.loyalty -= 1
        if self.tax_rate < 0.9:
            self.morale += 1
        if self.food < 0:
            self.morale -= 10
            self.population -= 2
        if self.morale <= 0 or self.population <= 0:
            self.collapsed = True

    def apply_action(self, action, chronicle):
        if action == "build_farm" and self.gold >= 25:
            self.gold -= 25
            self.farms += 1
            chronicle.add("New farms expand the kingdom's food supply.")
        elif action == "build_mine" and self.gold >= 30:
            self.gold -= 30
            self.mines += 1
            chronicle.add("Miners open a new vein of ore.")
        elif action == "build_infra" and self.gold >= 40:
            self.gold -= 40
            self.infrastructure += 1
            self.morale += 2
            chronicle.add("Roads and granaries improve efficiency.")
        elif action == "feast" and self.food >= 15:
            self.food -= 15
            self.morale += 8
            self.loyalty += 4
            chronicle.add("A grand feast lifts spirits across the realm.")
        elif action == "tax" and self.loyalty > 10:
            self.gold += 15
            self.tax_rate = min(self.tax_rate + 0.1, 1.5)
            self.morale -= 4
            self.loyalty -= 3
            chronicle.add("Extra taxes fill the treasury but anger the people.")
        elif action == "recruit" and self.gold >= 20:
            self.gold -= 20
            self.army += 4
            self.fear += 2
            chronicle.add("New soldiers bolster the royal army.")
        else:
            chronicle.add("The council postpones major decisions.")

    def display(self):
        print(
            "Pop:{pop} Food:{food} Gold:{gold} Morale:{morale} Loyalty:{loyalty} "
            "Army:{army} Farms:{farms} Mines:{mines} Infra:{infra}"
            .format(
                pop=self.population,
                food=int(self.food),
                gold=self.gold,
                morale=self.morale,
                loyalty=self.loyalty,
                army=self.army,
                farms=self.farms,
                mines=self.mines,
                infra=self.infrastructure,
            )
        )
