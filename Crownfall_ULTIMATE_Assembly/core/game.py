
import pygame, json, os
from world.world import World
from ui.hud import HUD

class Game:
    def __init__(self, config):
        self.ironman = config["ironman"]
        self.world = World(config["faction"])
        self.hud = HUD()
        self.save_path = "saves/ironman.json" if self.ironman else "saves/save.json"
        os.makedirs("saves", exist_ok=True)

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.save()

    def update(self, dt):
        self.world.update(dt)
        if self.ironman:
            self.save()

    def draw(self, screen):
        screen.fill((20,20,30))
        self.world.draw(screen)
        self.hud.draw(screen, self.world)

    def save(self):
        with open(self.save_path, "w") as f:
            json.dump(self.world.serialize(), f)
