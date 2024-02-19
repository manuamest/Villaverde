import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Tree(Generic):
	def __init__(self, pos, surf, groups, name, player_add):
		super().__init__(pos, surf, groups)

		# tree attributes
		self.health = 3
		self.alive = True
		stump_path = f'code/sprites/ambiente/ambiente_verano/{"arbol1" if name == "arbol1" else ("arbol2" if name == "arbol2" else "arbol3")}.png'
		self.stump_surf = pygame.image.load(stump_path).convert_alpha()

		self.player_add = player_add

		# sounds
		#self.axe_sound = pygame.mixer.Sound('../audio/axe.mp3')

	def damage(self):
		
		# damaging the tree
		self.health -= 1

		# play sound
		# self.axe_sound.play()

	def check_death(self):
		if self.health <= 0:
			self.image = self.stump_surf
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)
			self.alive = False
			self.player_add('Madera')

	def update(self,dt):
		if self.alive:
			self.check_death()