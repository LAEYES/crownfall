import pygame

TILE_SIZE = 32

class Building:
    def __init__(self, x: int, y: int, image_path: str):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()

    def draw(self, screen, cam_x, cam_y):
        screen.blit(self.image, (self.x * TILE_SIZE - cam_x, self.y * TILE_SIZE - cam_y))

    def tile_pos(self):
        return self.x, self.y


class Farm(Building):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "assets/building_farm.png")

    def produce(self):
        return 2


class Barracks(Building):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "assets/building_barracks.png")
