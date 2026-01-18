import pygame
from world.map import WorldMap
from world.agent import Agent
from world.faction import Faction
from world.building import Farm, Barracks

class World:
    def __init__(self):
        self.tile_size = 32

        # Carte
        self.map = WorldMap(50, 30, self.tile_size)

        # Caméra
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 300  # pixels/sec

        # Factions
        self.factions = [
            Faction("Kingdom", "neutral", (80, 120, 255)),
            Faction("Empire", "hostile", (200, 80, 80)),
        ]

        # Agents (positions volontairement visibles)
        self.agents = [
            Agent(5, 5, self.factions[0]),
            Agent(8, 6, self.factions[1]),
        ]

        # Bâtiments
        self.buildings = []

        # Sélection
        self.selected_agent = None
        self.selected_building = None

        # Placement mode
        self.placement_active = False
        self.placement_type = None  # "farm" or "barracks"
        self.ghost_image = None

    def screen_to_tile(self, mx, my):
        tx = int((mx + self.camera_x) // self.tile_size)
        ty = int((my + self.camera_y) // self.tile_size)
        return tx, ty

    def is_tile_in_bounds(self, tx, ty):
        return 0 <= tx < self.map.width and 0 <= ty < self.map.height

    def is_tile_free(self, tx, ty):
        if not self.is_tile_in_bounds(tx, ty):
            return False
        for b in self.buildings:
            if (b.x, b.y) == (tx, ty):
                return False
        return True

    def start_placement(self, btype: str):
        self.placement_active = True
        self.placement_type = btype
        # Précharge image fantôme
        path = "assets/building_farm.png" if btype == "farm" else "assets/building_barracks.png"
        self.ghost_image = pygame.image.load(path).convert_alpha()
        self.ghost_image.set_alpha(160)

    def cancel_placement(self):
        self.placement_active = False
        self.placement_type = None
        self.ghost_image = None

    def confirm_placement(self, tx, ty):
        if not self.placement_active:
            return False
        if not self.is_tile_free(tx, ty):
            return False
        if self.placement_type == "farm":
            self.buildings.append(Farm(tx, ty))
        elif self.placement_type == "barracks":
            self.buildings.append(Barracks(tx, ty))
        else:
            return False
        self.cancel_placement()
        return True

    def select_at_tile(self, tx, ty):
        # Priorité aux agents
        self.selected_agent = None
        self.selected_building = None
        for a in self.agents:
            if (a.x, a.y) == (tx, ty):
                self.selected_agent = a
                return
        for b in self.buildings:
            if (b.x, b.y) == (tx, ty):
                self.selected_building = b
                return

    def handle_camera(self, keys, dt):
        if keys[pygame.K_a]:
            self.camera_x -= self.camera_speed * dt
        if keys[pygame.K_d]:
            self.camera_x += self.camera_speed * dt
        if keys[pygame.K_w]:
            self.camera_y -= self.camera_speed * dt
        if keys[pygame.K_s]:
            self.camera_y += self.camera_speed * dt

        # Clamp caméra (empêche sortie de map)
        max_x = self.map.width * self.tile_size - 1024
        max_y = self.map.height * self.tile_size - 576
        self.camera_x = max(0, min(self.camera_x, max_x))
        self.camera_y = max(0, min(self.camera_y, max_y))

    def update(self, dt):
        for a in self.agents:
            a.update(dt)

    def draw(self, screen):
        self.map.draw(screen, self.camera_x, self.camera_y)

        # Dessine bâtiments
        for b in self.buildings:
            b.draw(screen, self.camera_x, self.camera_y)

        # Dessine agents
        for a in self.agents:
            a.draw(screen, self.camera_x, self.camera_y)

        # Surbrillance sélection
        if self.selected_agent is not None:
            x, y = self.selected_agent.x * self.tile_size - self.camera_x, self.selected_agent.y * self.tile_size - self.camera_y
            pygame.draw.rect(screen, (255, 255, 0), (x, y, self.tile_size, self.tile_size), 2)
        elif self.selected_building is not None:
            x, y = self.selected_building.x * self.tile_size - self.camera_x, self.selected_building.y * self.tile_size - self.camera_y
            pygame.draw.rect(screen, (0, 255, 255), (x, y, self.tile_size, self.tile_size), 2)

        # Fantôme placement
        if self.placement_active and self.ghost_image is not None:
            mx, my = pygame.mouse.get_pos()
            tx, ty = self.screen_to_tile(mx, my)
            px, py = tx * self.tile_size - self.camera_x, ty * self.tile_size - self.camera_y
            valid = self.is_tile_free(tx, ty)
            # image semi-transparente
            screen.blit(self.ghost_image, (px, py))
            # overlay vert/rouge
            overlay = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            overlay.fill((0, 200, 0, 80) if valid else (200, 0, 0, 80))
            screen.blit(overlay, (px, py))
