import pygame
from world.world import World
from ui.ui import UI
from systems.save_manager import SaveManager

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crownfall v1.0")

clock = pygame.time.Clock()
world = World()
ui = UI()
saves = SaveManager()

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                saves.save(world)
            if event.key == pygame.K_F9:
                saves.load(world)
            # Toggle placement: B for Farm, Shift+B for Barracks
            if event.key == pygame.K_b:
                mods = pygame.key.get_mods()
                if world.placement_active:
                    world.cancel_placement()
                else:
                    world.start_placement("barracks" if mods & pygame.KMOD_SHIFT else "farm")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            tx, ty = world.screen_to_tile(mx, my)
            if event.button == 1:
                # Left click: confirm placement or select
                if world.placement_active:
                    world.confirm_placement(tx, ty)
                else:
                    world.select_at_tile(tx, ty)
            elif event.button == 3:
                # Right click: cancel placement
                if world.placement_active:
                    world.cancel_placement()

    # 🔑 LIGNE CRITIQUE MANQUANTE
    keys = pygame.key.get_pressed()
    world.handle_camera(keys, dt)

    world.update(dt)

    screen.fill((18, 18, 25))
    world.draw(screen)
    ui.draw(screen, world)

    pygame.display.flip()

pygame.quit()
