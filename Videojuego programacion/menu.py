import pygame
import sys
import random
from game import Game
from settings import WIDTH, HEIGHT

def show_controls(screen, clock):
    font = pygame.font.SysFont("arial", 30, bold=True)
    button_font = pygame.font.SysFont("arial", 24)

    particles = []

    def draw_particles():
        for particle in particles:
            pygame.draw.circle(screen, (255, 0, 0), particle[:2], particle[2])
            particle[0] += random.uniform(-1, 1)
            particle[1] += particle[3]
            particle[2] -= 0.1
        particles[:] = [p for p in particles if p[2] > 0]

    controls_text = [
        "WASD - Moverse",
        "Click Derecho - Disparar",
        "Click Izquierdo - Seleccionar habilidad",
        "P - Pausar",
        "Esc - Volver al menú",
    ]

    waiting = True
    while waiting:
        screen.fill((20, 20, 20))
        draw_particles()

        if random.randint(0, 10) > 8:
            particles.append([
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.randint(2, 5),
                random.uniform(1, 3)
            ])

        title = font.render("Controles", True, (180, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, line in enumerate(controls_text):
            text_surface = button_font.render(line, True, (200, 200, 200))
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 150 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

        clock.tick(60)


def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Untoter Menu")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 30, bold=True)
    button_font = pygame.font.SysFont("arial", 24)

    hover_sound = pygame.mixer.Sound("sounds/hover_sound.mp3")
    select_sound = pygame.mixer.Sound("sounds/select_sound.mp3")

    pygame.mixer.music.load("sounds/menu_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    particles = []

    def draw_particles():
        for particle in particles:
            pygame.draw.circle(screen, (255, 0, 0), particle[:2], particle[2])
            particle[0] += random.uniform(-1, 1)
            particle[1] += particle[3]
            particle[2] -= 0.1
        particles[:] = [p for p in particles if p[2] > 0]

    def draw_text(text, y, is_hovered):
        color = (255, 255, 255) if is_hovered else (150, 150, 150)
        text_surface = button_font.render(text, True, color)
        rect = text_surface.get_rect(center=(WIDTH // 2, y))
        screen.blit(text_surface, rect)
        return rect


    selected_index = 0
    options = ["Jugar", "Controles", "Salir"]

    while True:
        screen.fill((20, 20, 20))
        draw_particles()

        if random.randint(0, 10) > 8:
            particles.append([
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.randint(2, 5),
                random.uniform(1, 3)
            ])

        title = font.render("Untoter Menu", True, (180, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        button_rects = []
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(options):
            rect = draw_text(option, 150 + i * 40, rect.collidepoint(mouse_pos) if i < len(button_rects) else False)
            button_rects.append(rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                    hover_sound.play()
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                    hover_sound.play()
                elif event.key == pygame.K_RETURN:
                    select_sound.play()
                    if options[selected_index] == "Jugar":
                        game = Game.get_instance()
                        result = game.run()
                        if result == "menu":
                            continue
                    elif options[selected_index] == "Controles":
                        show_controls(screen, clock)
                    elif options[selected_index] == "Salir":
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        select_sound.play()
                        selected_index = i
                        if options[selected_index] == "Jugar":
                            game = Game.get_instance()
                            result = game.run()
                            if result == "menu":
                                continue
                        elif options[i] == "Controles":
                            show_controls(screen, clock)
                        elif options[i] == "Salir":
                            pygame.quit()
                            sys.exit()

        clock.tick(60)
