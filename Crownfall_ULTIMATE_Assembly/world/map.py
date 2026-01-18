import pygame

class WorldMap:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.tile_grass = pygame.image.load(
            "assets/tile_grass.png"
        ).convert_alpha()

    def draw(self, screen, cam_x, cam_y):
        start_x = int(cam_x // self.tile_size)
        start_y = int(cam_y // self.tile_size)

        tiles_x = screen.get_width() // self.tile_size + 2
        tiles_y = screen.get_height() // self.tile_size + 2

        for y in range(start_y, start_y + tiles_y):
            for x in range(start_x, start_x + tiles_x):
                if 0 <= x < self.width and 0 <= y < self.height:
                    screen.blit(
                        self.tile_grass,
                        (
                            x * self.tile_size - cam_x,
                            y * self.tile_size - cam_y,
                        ),
                    )
