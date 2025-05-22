# game.py

import pygame
import random
from player import Player
from enemy import Enemy
from enemy import Boss
from upgrade import Upgrade


from config import WIDTH, HEIGHT

FPS = 60

class Game:
    _instance = None  # Atributo de clase para la instancia única

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        if Game._instance is None:
            Game()
        return Game._instance

    def __init__(self):
        # Evitar re-inicialización si ya existe la instancia
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Untoter")
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Untoter")
        self.clock = pygame.time.Clock()
        
        # Música de fondo
        pygame.mixer.music.load('sounds/background_music.mp3')
        pygame.mixer.music.set_volume(0.5)  # Controla el volumen de la música
        pygame.mixer.music.play(-1, 0.0)  # -1 para que se repita indefinidamente

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.player = Player(WIDTH // 2, HEIGHT // 2, self.all_sprites, self.projectiles)
        self.all_sprites.add(self.player)

        self.enemy_speed = 2
        self.spawn_enemies(5)

        self.font = pygame.font.SysFont(None, 28)
        self.score = 0
        self.level = 1

        self.selecting_upgrade = False
        self.upgrade_options = []

    # Pantalla de selección de mejoras

    def show_upgrade_screen(self):
        self.selecting_upgrade = True
        self.upgrade_options = Upgrade.get_random_upgrades(self.player)

        while self.selecting_upgrade:
            self.clock.tick(60)
            self.screen.fill((20, 20, 40))

            # Título con sombra
            title_text = "¡Selecciona una mejora!"
            shadow_color = (0, 0, 0)
            title_color = (255, 0, 0)
            self.draw_text(title_text, WIDTH // 2 - 102, 98, shadow_color, size=36)
            self.draw_text(title_text, WIDTH // 2 - 100, 100, title_color, size=36)

            for i, upgrade in enumerate(self.upgrade_options):
                rect = pygame.Rect(100 + i * 220, 200, 200, 120)

                # Fondo degradado
                pygame.draw.rect(self.screen, (30, 30, 100), rect)
                pygame.draw.rect(self.screen, (50, 50, 150), rect.inflate(-10, -10))

                # Borde brillante
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

                # Texto de mejora
                self.draw_text(upgrade.name, rect.x + 10, rect.y + 10, (255, 255, 255), size=24)
                self.draw_text(upgrade.description, rect.x + 10, rect.y + 50, (200, 200, 200), size=16)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.selecting_upgrade = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for i, upgrade in enumerate(self.upgrade_options):
                        rect = pygame.Rect(100 + i * 220, 200, 200, 120)
                        if rect.collidepoint(mx, my):
                            upgrade.apply()
                            pygame.mixer.Sound('sounds/upgrade_selected.mp3').play()  # Sonido al seleccionar mejora
                            self.selecting_upgrade = False

    # Spawn de enemigos

    def spawn_enemies(self, count):
        for _ in range(count):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            while abs(x - self.player.rect.x) < 100 and abs(y - self.player.rect.y) < 100:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
            enemy_type = random.choice(["normal", "tank", "fast"])
            enemy = Enemy(x, y, self.player, enemy_type=enemy_type, speed=self.enemy_speed)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        spawn_sound = pygame.mixer.Sound('sounds/enemy_spawn.mp3')
        spawn_sound.set_volume(0.2) 
        spawn_sound.play()

    # Pantalla de Game Over

    def draw_text(self, text, x, y, color=(255, 255, 255), size=None):
        font = self.font if size is None else pygame.font.SysFont(None, size)
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    # Dibujo de la barra de vida

    def draw_health_bar(self, surface, x, y, health, max_health, bar_width=200):
        bar_height = 20
        fill = (health / max_health) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)


    # Pantalla de Game Over
    def game_over_screen(self):
        # Fondo con degradado
        for i in range(HEIGHT):
            color = (i // 3, 0, 0)  # Degradado de rojo oscuro a negro
            pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))

        # Mensajes en pantalla
        game_over_text = "GAME OVER"
        score_text = f"Tu puntaje fue: {self.score}"
        restart_text = "Presiona R para reiniciar o ESC para salir"

        # Título con sombra
        shadow_color = (0, 0, 0)
        title_color = (255, 50, 50)
        title_font = pygame.font.SysFont(None, 64)
        title_width, title_height = title_font.size(game_over_text)
        self.draw_text(game_over_text, (WIDTH - title_width) // 2 - 2, (HEIGHT - title_height) // 2 - 102, shadow_color, size=64)
        self.draw_text(game_over_text, (WIDTH - title_width) // 2, (HEIGHT - title_height) // 2 - 100, title_color, size=64)

        # Puntaje
        score_font = pygame.font.SysFont(None, 32)
        score_width, score_height = score_font.size(score_text)
        self.draw_text(score_text, (WIDTH - score_width) // 2, (HEIGHT - score_height) // 2, (255, 255, 255), size=32)

        # Instrucciones
        restart_font = pygame.font.SysFont(None, 24)
        restart_width, restart_height = restart_font.size(restart_text)
        self.draw_text(restart_text, (WIDTH - restart_width) // 2, (HEIGHT - restart_height) // 2 + 50, (200, 200, 200), size=24)

        # Animación de un borde parpadeante
        border_color = (255, 50, 50) if pygame.time.get_ticks() % 1000 < 500 else (100, 0, 0)
        pygame.draw.rect(self.screen, border_color, (50, 50, WIDTH - 100, HEIGHT - 100), 5)

        # Actualizar pantalla
        pygame.display.flip()

        # Esperar interacción del jugador
        self.wait_for_input()

    def wait_for_input(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()  # Reinicia el juego
                        self.run()       # Corre el juego de nuevo
                        return
                    elif event.key == pygame.K_m:
                        return "menu"    # Retorna control al menú
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                        # Cambiar música para la pantalla de Game Over
                        pygame.mixer.music.load('sounds/menu_music.mp3')
                        pygame.mixer.music.play(-1, 0.0)  # Reproducir indefinidamente

    def increase_difficulty(self):
        if self.score > 0 and self.score % 5 == 0:
            self.level += 1
            self.enemy_speed += 0.5
            print(f"¡Nivel {self.level}! Velocidad enemigos: {self.enemy_speed}")

            # Agregar jefe cada 5 niveles
            if self.level % 5 == 0:
                self.spawn_boss()

            self.show_upgrade_screen()  # Mostrar pantalla de mejoras al subir de nivel

    def spawn_boss(self):
        boss = Boss(WIDTH // 2, HEIGHT // 2, self.player)
        self.enemies.add(boss)
        self.all_sprites.add(boss)
        pygame.mixer.music.load('sounds/boss_music.mp3')  # Música de jefe
        pygame.mixer.music.play(-1, 0.0)  # Música de jefe que se repite

        # Monitorear la muerte del jefe
        def check_boss_status():
            if not boss.alive():
                pygame.mixer.music.load('sounds/background_music.mp3')  # Volver a la música de fondo
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1, 0.0)

        boss.update = lambda: (Boss.update(boss), check_boss_status())

    def apply_upgrade(self):
        upgrade = random.choice(['faster_shooting', 'more_damage', 'regen'])
        if upgrade == 'faster_shooting':
            self.player.shoot_delay = max(100, self.player.shoot_delay - 50)
            print("🔥 Mejora: Disparo más rápido")
        elif upgrade == 'more_damage':
            self.player.damage += 5
            print("💥 Mejora: Más daño")
        elif upgrade == 'regen':
            self.player.health = min(100, self.player.health + 20)
            print("❤️ Mejora: Regeneración de vida")

    def reset_game(self):
        # Resetear atributos
        self.all_sprites.empty()
        self.enemies.empty()
        self.projectiles.empty()

        self.player = Player(WIDTH // 2, HEIGHT // 2, self.all_sprites, self.projectiles)
        self.all_sprites.add(self.player)

        self.score = 0
        self.level = 1
        self.enemy_speed = 2
        self.spawn_enemies(5)

        # Reproducir música de fondo
        pygame.mixer.music.load('sounds/background_music.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1, 0.0)


    def draw_enemy_health_bar(self, surface, enemy, bar_width=None):
        bar_width = bar_width if bar_width is not None else enemy.rect.width // 10  # Reduce aún más el ancho de la barra
        bar_height = 4  # Mantiene la altura de la barra
        if enemy.enemy_type == "tank":
            health_ratio = enemy.health / 100
        elif enemy.enemy_type == "normal":
            health_ratio = enemy.health / 50
        elif enemy.enemy_type == "boss":
            health_ratio = enemy.health / 200
        else:
            health_ratio = enemy.health / 30  # fallback
        fill = int(bar_width * health_ratio)
        outline_rect = pygame.Rect(enemy.rect.x + (enemy.rect.width - bar_width) // 2, enemy.rect.y - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(enemy.rect.x + (enemy.rect.width - bar_width) // 2, enemy.rect.y - 10, fill, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

    # Método para la pantalla de pausa
    def pause_screen(self):
        paused = True
        while paused:
            self.clock.tick(FPS)
            self.screen.fill((30, 30, 60))  # Fondo más atractivo

            # Título con sombra
            pause_text = "Juego en Pausa"
            shadow_color = (0, 0, 0)
            title_color = (255, 215, 0)
            title_font = pygame.font.SysFont(None, 48)
            title_width, title_height = title_font.size(pause_text)
            self.draw_text(pause_text, (WIDTH - title_width) // 2 - 2, (HEIGHT - title_height) // 2 - 102, shadow_color, size=48)
            self.draw_text(pause_text, (WIDTH - title_width) // 2, (HEIGHT - title_height) // 2 - 100, title_color, size=48)

            # Opciones
            resume_text = "Presiona P para continuar"
            menu_text = "Presiona R para reiniciar"
            quit_text = "Presiona ESC para salir del juego"
            resume_font = pygame.font.SysFont(None, 24)
            resume_width, resume_height = resume_font.size(resume_text)
            menu_width, menu_height = resume_font.size(menu_text)
            quit_width, quit_height = resume_font.size(quit_text)
            self.draw_text(resume_text, (WIDTH - resume_width) // 2, HEIGHT // 2, (200, 200, 200), size=24)
            self.draw_text(menu_text, (WIDTH - menu_width) // 2, HEIGHT // 2 + 40, (200, 200, 200), size=24)
            self.draw_text(quit_text, (WIDTH - quit_width) // 2, HEIGHT // 2 + 80, (200, 200, 200), size=24)

            # Animación de borde parpadeante
            border_color = (255, 215, 0) if pygame.time.get_ticks() % 1000 < 500 else (100, 100, 100)
            pygame.draw.rect(self.screen, border_color, (50, 50, WIDTH - 100, HEIGHT - 100), 5)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Reanudar el juego
                        paused = False
                    elif event.key == pygame.K_r:  # Reiniciar
                        self.reset_game()  # Reseteo del juego
                        paused = False
                        return  # Salir de la pausa para que el main pueda llamar a show_menu
                    elif event.key == pygame.K_ESCAPE:  # Salir del juego
                        pygame.quit()
                        exit()

    # Modificación del método run para incluir la pausa
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Activar la pausa
                        self.pause_screen()

            keys_pressed = pygame.key.get_pressed()
            self.player.update(keys_pressed)
            self.enemies.update()
            self.projectiles.update()

            # Colisiones: proyectil vs enemigo
            for enemy in self.enemies:
                for projectile in self.projectiles:
                    if enemy.rect.colliderect(projectile.rect):
                        enemy.take_damage(projectile.damage)
                        projectile.kill()
                        self.score += 1
                        if not enemy.alive():
                            self.increase_difficulty()
                            self.spawn_enemies(1)

            enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            for enemy in enemy_hits:
                self.player.take_damage(20)

            if self.player.health <= 0:
                self.game_over_screen()
                self.reset_game()

            # Dibujado
            self.screen.fill((30, 30, 30))
            self.all_sprites.draw(self.screen)

            for enemy in self.enemies:
                self.draw_enemy_health_bar(self.screen, enemy)
                bar_width = 50 if enemy.enemy_type != "boss" else 200  
                self.draw_enemy_health_bar(self.screen, enemy, bar_width=bar_width)

            self.draw_health_bar(self.screen, 10, 10, self.player.health, 100)
            self.draw_text(f"Puntaje: {self.score}", 10, 40)
            self.draw_text(f"Nivel: {self.level}", 10, 65)
            pygame.display.flip()

            # Condición de Game Over
            if self.player.health <= 0:
                result = self.game_over_screen()
                if result == "menu":
                    return 
                else:
                    continue

        pygame.quit()

