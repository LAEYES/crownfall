
import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 14)

    def draw(self, screen, world):
        y = 5
        for f in world.factions:
            txt = self.font.render(
                f"{f.name}: {f.relation} | Gold {int(f.gold)}",
                True, (230,230,230)
            )
            screen.blit(txt, (5,y))
            y += 18
