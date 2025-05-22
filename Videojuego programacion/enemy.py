# enemy.py
import pygame
from config import WIDTH, HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, target, enemy_type="normal", speed=2):
        super().__init__()
        self.enemy_type = enemy_type
        self.target = target
        self.speed = speed

        # Cargar imágenes específicas para cada tipo de enemigo
        self.images = self.load_images()
        self.attack_images = self.load_attack_images()
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150  # milisegundos entre cuadros normales
        self.attack_frame_rate = 400  # milisegundos entre cuadros de animación de ataque

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hit_sound = pygame.mixer.Sound('sounds/enemy_hit.mp3')  # Sonido de golpe

        if enemy_type == "tank":
            self.health = 100
            self.speed = 1
            self.damage = 15
        elif enemy_type == "fast":
            self.health = 30
            self.speed = 3.5
            self.damage = 5
        else:  # normal
            self.health = 50
            self.damage = 10

        self.attack_range = 50  # Rango de ataque en píxeles
        self.last_attack_time = 0
        self.attack_delay = 1000  # Tiempo entre ataques en milisegundos
        self.is_attacking = False  # Estado de ataque

    def load_images(self):
        frames = []
        if self.enemy_type == "tank":
            for i in range(1, 6):
                image = pygame.image.load(f'assets/enemies/tank/tank{i}.png').convert_alpha()
                frames.append(image)
        elif self.enemy_type == "fast":
            for i in range(1, 6):
                image = pygame.image.load(f'assets/enemies/fast/fast{i}.png').convert_alpha()
                frames.append(image)
        else:  # normal
            for i in range(1, 6):
                image = pygame.image.load(f'assets/enemies/normal/normal{i}.png').convert_alpha()
                frames.append(image)
        return frames

    def load_attack_images(self):
        frames = []
        if self.enemy_type == "tank":
            for i in range(1, 2): 
                image = pygame.image.load(f'assets/enemies/tank/attack{i}.png').convert_alpha()
                frames.append(image)
        elif self.enemy_type == "fast":
            for i in range(1, 2):
                image = pygame.image.load(f'assets/enemies/fast/attack{i}.png').convert_alpha()
                frames.append(image)
        else:  # normal
            for i in range(1, 2):
                image = pygame.image.load(f'assets/enemies/normal/attack{i}.png').convert_alpha()
                frames.append(image)
        return frames

    def update(self):
        # Movimiento hacia el objetivo
        if not self.is_attacking:
            direction = pygame.math.Vector2(
                self.target.rect.centerx - self.rect.centerx,
                self.target.rect.centery - self.rect.centery
            )
            if direction.length() != 0:
                direction = direction.normalize()
                self.rect.x += direction.x * self.speed
                self.rect.y += direction.y * self.speed

        # Animación
        self.animate()

        # Ataque al jugador si está cerca
        self.attack()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if self.is_attacking:
                self.current_frame = (self.current_frame + 1) % len(self.attack_images)
                self.image = self.attack_images[self.current_frame]
                # Finalizar animación de ataque
                if self.current_frame == len(self.attack_images) - 1:
                    self.is_attacking = False
            else:
                self.current_frame = (self.current_frame + 1) % len(self.images)
                self.image = self.images[self.current_frame]

    def attack(self):
        now = pygame.time.get_ticks()
        distance_to_target = pygame.math.Vector2(
            self.target.rect.centerx - self.rect.centerx,
            self.target.rect.centery - self.rect.centery
        ).length()

        if distance_to_target <= self.attack_range and now - self.last_attack_time > self.attack_delay:
            self.is_attacking = True  # Activar animación de ataque
            print(f"Enemy attacking! Player health before: {self.target.health}")
            self.target.take_damage(self.damage)
            print(f"Player health after: {self.target.health}")
            self.last_attack_time = now

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            self.hit_sound.play()  # Reproduce el sonido cuando el enemigo muere

class Boss(Enemy):
    def __init__(self, x, y, target):
        super().__init__(x, y, target, enemy_type="boss", speed=1.5)
        self.health = 200  # Más vida
        self.damage = 20  # Daño más alto
        self.images = self.load_images()  # Cargar imágenes específicas del jefe
        self.attack_images = self.load_attack_images()  # Cargar imágenes de ataque del jefe
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        frames = []
        for i in range(1, 6):  
            image = pygame.image.load(f'assets/enemies/boss/boss{i}.png').convert_alpha()
            frames.append(image)
        return frames

    def load_attack_images(self):
        frames = []
        for i in range(1, 2):  
            image = pygame.image.load(f'assets/enemies/boss/attack{i}.png').convert_alpha()
            frames.append(image)
        return frames
