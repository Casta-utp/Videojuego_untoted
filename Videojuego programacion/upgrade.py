# upgrade.py

import pygame
import random

class Upgrade:
    def __init__(self, name, description, apply_func):
        self.name = name
        self.description = description
        self.apply = apply_func

    @staticmethod
    def get_random_upgrades(player):
        return random.sample([
            Upgrade("Más Daño ++", "Aumenta el daño de proyectiles", lambda: setattr(player, 'damage', player.damage + 5)),
            Upgrade("Vida +20", "Recupera 20 puntos de vida", lambda: setattr(player, 'health', min(player.health + 20, 100))),
            Upgrade("Disparo Rápido ++", "Reduce el tiempo entre disparos", lambda: setattr(player, 'shoot_delay', max(100, player.shoot_delay - 50))),
            Upgrade("Velocidad ++", "Aumenta ligeramente la velocidad", lambda: setattr(player, 'speed', player.player_speed + 1)),
        ], 3)
