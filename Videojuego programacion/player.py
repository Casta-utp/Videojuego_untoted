# player.py

import pygame
from projectile import Projectile

SHOOT_DELAY = 500  # ms
MAX_HEALTH = 100

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, projectiles_group):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.last_shot = pygame.time.get_ticks()
        self.all_sprites = all_sprites
        self.projectiles_group = projectiles_group

        self.health = MAX_HEALTH
        self.shoot_delay = 500  # milisegundos
        self.damage = 10
        self.last_shot = pygame.time.get_ticks()
        self.shoot_sound = pygame.mixer.Sound('sounds/shoot_sound.mp3')  # Efecto de sonido

        self.player_speed = 5

        self.images = self.load_images()
        self.shoot_images = self.load_shoot_images()
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # milisegundos entre cuadros

        self.is_shooting = False
        self.shoot_animation_time = 400  # Duración de la animación de disparo en ms
        self.shoot_animation_start = 0

        self.invulnerability_time = 2000  # Tiempo de invulnerabilidad en ms
        self.last_damage_time = 0

        self.is_damaged = False  # Indica si el jugador está en estado de daño
        self.damage_effect_time = 200  # Duración del efecto de daño en ms

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            projectile = Projectile(self.rect.centerx, self.rect.centery, mouse_x, mouse_y, self.damage)
            self.projectiles_group.add(projectile)
            self.all_sprites.add(projectile)
            self.last_shot = now
            self.shoot_sound.set_volume(0.5)
            self.shoot_sound.play()

            # Activar animación de disparo
            self.is_shooting = True
            self.shoot_animation_start = now

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.player_speed
        if keys_pressed[pygame.K_s] and self.rect.bottom < pygame.display.get_surface().get_height():
            self.rect.y += self.player_speed
        if keys_pressed[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.player_speed
            self.image = pygame.transform.flip(self.images[self.current_frame], True, False)  # Voltear hacia la izquierda
        if keys_pressed[pygame.K_d] and self.rect.right < pygame.display.get_surface().get_width():
            self.rect.x += self.player_speed
            self.image = self.images[self.current_frame]  # Restaurar imagen original (hacia la derecha)

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[2]:
            self.shoot()

        self.animate()


    def take_damage(self, amount):
        now = pygame.time.get_ticks()
        if now - self.last_damage_time > self.invulnerability_time:
            self.health -= amount
            self.last_damage_time = now
            self.is_damaged = True  # Activar efecto de daño
            if self.health <= 0:
                self.kill()

    def load_images(self):
        frames = []
        for i in range(1, 7):  # en total hay 5 imágenes
            image = pygame.image.load(f'assets/player/player{i}.png').convert_alpha()
            frames.append(image)
        return frames

    def load_shoot_images(self):
        frames = []
        for i in range(1, 2):
            image = pygame.image.load(f'assets/player/shoot{i}.png').convert_alpha()
            frames.append(image)
        return frames

    def animate(self):
        now = pygame.time.get_ticks()
        if self.is_damaged:
            # Efecto de parpadeo
            if (now // 100) % 2 == 0:  # Alternar visibilidad cada 100 ms
                self.image.set_alpha(128)  # Semitransparente
            else:
                self.image.set_alpha(255)  # Totalmente visible

            # Terminar efecto de daño después de un tiempo
            if now - self.last_damage_time > self.damage_effect_time:
                self.is_damaged = False
                self.image.set_alpha(255)  # Restaurar visibilidad completa
        elif self.is_shooting:
            # Animación de disparo
            if now - self.shoot_animation_start < self.shoot_animation_time:
                self.current_frame = (now // self.frame_rate) % len(self.shoot_images)
                self.image = self.shoot_images[self.current_frame]
            else:
                self.is_shooting = False  # Terminar animación de disparo
        else:
            # Animación normal
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images)
                self.image = self.images[self.current_frame]
