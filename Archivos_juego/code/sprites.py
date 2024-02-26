import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy()

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add, inventory):
        super().__init__(pos, surf, groups)
        self.name = name
        self.player_add = player_add
        self.inventory = inventory
        self.stump_surf = pygame.image.load(f'code/sprites/ambiente/ambiente_verano/{"tronco1" if name == "arbol1" else ("tronco2" if name == "arbol2" else "tronco3")}.png').convert_alpha()
        self.alive = True
        self.health = 1

    def damage(self):
        self.health -= 1

    def check_death(self):
        if self.health <= 0:
            # Ajustar posición inicial del sprite  
            self.rect.y += 20
            self.rect.x -= 20
            self.image = self.stump_surf
            # Ajustar el rectángulo para el tocón
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy()
            self.alive = False
            self.inventory.añadir_madera()

    def update(self, dt):
        if self.alive:
            self.check_death()
