
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
        self.housing = 1
        self.unrest = 10
        self.stability = 60
        self.tax_rate = 1.0
        self.focus = "balanced"
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
        focus_food = 1.0
        focus_gold = 1.0
        if self.focus == "welfare":
            focus_food = 1.1
        elif self.focus == "economy":
            focus_gold = 1.15
        self.food += food_gain * morale_factor * focus_food
        self.gold += int(gold_gain * morale_factor * focus_gold)
        self.population += int(self.housing * 0.3 * morale_factor)

    def consume(self, season):
        season_food_need = {"Winter": 1.1}
        self.food -= self.population * 0.7 * season_food_need.get(season, 1.0)
        if self.tax_rate > 1.2:
            self.morale -= 2
            self.loyalty -= 1
            self.unrest += 2
        if self.tax_rate < 0.9:
            self.morale += 1
            self.unrest = max(0, self.unrest - 1)
        if self.focus == "military":
            self.morale = max(0, self.morale - 1)
            self.fear += 1
        if self.food < 0:
            self.morale -= 10
            self.population -= 2
            self.unrest += 3
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
        elif action == "build_housing" and self.gold >= 35:
            self.gold -= 35
            self.housing += 1
            self.morale += 3
            chronicle.add("New housing districts welcome more families.")
        elif action == "build_infra" and self.gold >= 40:
            self.gold -= 40
            self.infrastructure += 1
            self.morale += 2
            chronicle.add("Roads and granaries improve efficiency.")
        elif action == "feast" and self.food >= 15:
            self.food -= 15
            self.morale += 8
            self.loyalty += 4
            self.unrest = max(0, self.unrest - 2)
            chronicle.add("A grand feast lifts spirits across the realm.")
        elif action == "tax" and self.loyalty > 10:
            self.gold += 15
            self.tax_rate = min(self.tax_rate + 0.1, 1.5)
            self.morale -= 4
            self.loyalty -= 3
            self.unrest += 2
            chronicle.add("Extra taxes fill the treasury but anger the people.")
        elif action == "recruit" and self.gold >= 20:
            self.gold -= 20
            self.army += 4
            self.fear += 2
            self.stability += 1
            chronicle.add("New soldiers bolster the royal army.")
        elif action == "parade" and self.gold >= 10:
            self.gold -= 10
            self.morale += 4
            self.fear = max(0, self.fear - 1)
            chronicle.add("A royal parade inspires confidence in the crown.")
        elif action == "aid" and self.gold >= 15:
            self.gold -= 15
            self.unrest = max(0, self.unrest - 4)
            self.loyalty += 2
            chronicle.add("Relief aid calms unrest in the provinces.")
        elif action == "focus_economy":
            self.focus = "economy"
            self.loyalty -= 1
            chronicle.add("Guilds celebrate a new focus on commerce.")
        elif action == "focus_welfare":
            self.focus = "welfare"
            self.morale += 2
            chronicle.add("The crown prioritizes welfare and local aid.")
        elif action == "focus_military":
            self.focus = "military"
            self.fear += 2
            chronicle.add("Barracks expand as the realm turns to defense.")
        elif action == "focus_balanced":
            self.focus = "balanced"
            chronicle.add("The council restores a balanced policy.")
        else:
            chronicle.add("The council postpones major decisions.")

    def end_turn_adjustments(self, chronicle):
        self.stability = max(0, min(100, self.stability + (self.loyalty - 50) // 10))
        if self.unrest > 60:
            self.morale -= 4
            self.stability -= 3
            chronicle.add("Riots erupt, shaking the kingdom's stability.")
        if self.stability < 20:
            self.collapsed = True
            chronicle.add("The kingdom splinters under instability.")

    def display(self):
        print(
            "Pop:{pop} Food:{food} Gold:{gold} Morale:{morale} Loyalty:{loyalty} "
            "Army:{army} Farms:{farms} Mines:{mines} Infra:{infra} Housing:{housing} "
            "Unrest:{unrest} Stability:{stability} Focus:{focus}"
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
                housing=self.housing,
                unrest=self.unrest,
                stability=self.stability,
                focus=self.focus,
            )
        )
