# projectile.py

import pygame

PROJECTILE_SPEED = 7

from config import WIDTH, HEIGHT

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, damage):
        super().__init__()
        # Carga la imagen del proyectil y redimensiona
        original_image = pygame.image.load("assets/projectile/projectile.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.damage = damage

        direction = pygame.math.Vector2(target_x - x, target_y - y)
        if direction.length() == 0:
            direction = pygame.math.Vector2(1, 0)
        else:
            direction = direction.normalize()
        self.velocity = direction * self.speed

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):
            self.kill()
