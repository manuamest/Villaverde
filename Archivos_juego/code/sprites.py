import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy()

class Particle(Generic):
	def __init__(self, pos, surf, groups, z, duration = 200):
		super().__init__(pos, surf, groups, z)
		self.start_time = pygame.time.get_ticks()
		self.duration = duration

		# Crear la superficie de particulas
		mask = pygame.mask.from_surface(self.image)
		new_surf = mask.to_surface()
		new_surf.set_colorkey((0,0,0))
		self.image = new_surf

	def update(self, dt):
		time = pygame.time.get_ticks()
		if time - self.start_time > self.duration:
			self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, inventory, season=0):
        super().__init__(pos, surf, groups)
        self.visible = True
        self.name = name
        self.inventory = inventory
        self.visible_image = surf  # Almacena la imagen original
        if season == 0:
            self.stump_surf = pygame.image.load(f'code/sprites/ambiente/ambiente_primavera/{"tronco1" if name == "arbol1" else ("tronco2" if name == "arbol2" else "tronco3")}.png').convert_alpha()
        elif season == 1:
            self.stump_surf = pygame.image.load(f'code/sprites/ambiente/ambiente_verano/{"tronco1" if name == "arbol1" else ("tronco2" if name == "arbol2" else "tronco3")}.png').convert_alpha()
        elif season == 2:
            self.stump_surf = pygame.image.load(f'code/sprites/ambiente/ambiente_otoño/{"tronco1" if name == "arbol1" else ("tronco2" if name == "arbol2" else "tronco3")}.png').convert_alpha()
        else:
            self.stump_surf = pygame.image.load(f'code/sprites/ambiente/ambiente_invierno/{"tronco1" if name == "arbol1" else ("tronco2" if name == "arbol2" else "tronco3")}.png').convert_alpha()
        self.alive = True
        self.health = 1

    def damage(self):
        if self.visible == True:
            self.health -= 1

    def check_death(self):
        if self.visible == True:
            if self.health <= 0:
                # Ajustar posición inicial del sprite  
                self.rect.y += 20
                self.rect.x -= 20
                self.image = self.stump_surf
                self.visible_image = self.stump_surf
                # Ajustar el rectángulo para el tocón
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
                self.hitbox = self.rect.copy()
                self.alive = False
                self.inventory.añadir_madera()

    def make_invisible(self):
        self.visible = False
        self.image = pygame.image.load('code/sprites/invisible.png')

    def make_visible(self):
        self.image = self.visible_image  # Restaura la imagen original

    def update(self, dt):
        if self.alive:
            self.check_death()
