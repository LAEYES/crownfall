import pygame
import random

class Agent:
    def __init__(self, x, y, faction):
        self.x = x
        self.y = y
        self.faction = faction

        self.state = "idle"
        self.prev_state = "idle"

        self.move_timer = random.uniform(0.5, 1.2)

        # Animations
        if faction.relation == "hostile":
            self.animations = {
                "idle": [
                    pygame.image.load("assets/unit_soldier_idle.png").convert_alpha()
                ],
                "walk": [
                    pygame.image.load("assets/unit_soldier_idle.png").convert_alpha(),
                    pygame.image.load("assets/unit_soldier_walk.png").convert_alpha(),
                ],
            }
        else:
            self.animations = {
                "idle": [
                    pygame.image.load("assets/unit_farmer_idle.png").convert_alpha()
                ],
                "walk": [
                    pygame.image.load("assets/unit_farmer_idle.png").convert_alpha(),
                    pygame.image.load("assets/unit_farmer_walk.png").convert_alpha(),
                ],
            }

        self.frame_index = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.25

    def update(self, dt):
        self.move_timer -= dt
        moved = False

        if self.move_timer <= 0:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            if dx != 0 or dy != 0:
                self.x += dx
                self.y += dy
                moved = True

            self.move_timer = random.uniform(0.5, 1.2)

        # FSM logic
        self.state = "walk" if moved else "idle"

        # 🔑 RESET animation on state change
        if self.state != self.prev_state:
            self.frame_index = 0
            self.anim_timer = 0
            self.prev_state = self.state

        # Animation update (safe)
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index += 1

            if self.frame_index >= len(self.animations[self.state]):
                self.frame_index = 0

    def draw(self, screen, cam_x, cam_y):
        sprite = self.animations[self.state][self.frame_index]
        screen.blit(
            sprite,
            (
                self.x * 32 - cam_x,
                self.y * 32 - cam_y,
            ),
        )
