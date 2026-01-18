
import pygame

class MainMenu:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 32)
        self.options = ["New Game", "Ironman", "Quit"]
        self.index = 0

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.index = (self.index + 1) % len(self.options)
            if event.key == pygame.K_UP:
                self.index = (self.index - 1) % len(self.options)
            if event.key == pygame.K_RETURN:
                if self.options[self.index] == "Quit":
                    pygame.quit()
                    exit()
                return {
                    "ironman": self.options[self.index] == "Ironman",
                    "faction": "Kingdom"
                }

    def draw(self, screen):
        screen.fill((10,10,20))
        for i, opt in enumerate(self.options):
            c = (200,200,80) if i == self.index else (180,180,180)
            txt = self.font.render(opt, True, c)
            screen.blit(txt, (420, 200 + i*50))
