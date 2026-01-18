class Faction:
    def __init__(self, name, relation, color):
        self.name = name
        self.relation = relation   # "neutral", "hostile", "friendly"
        self.color = color         # couleur RGB pour affichage
        self.gold = 100
