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
        
        self.rect.inflate_ip(20, 20)
        self.hitbox.midleft = self.rect.midleft 
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
        if self.visible:
            self.health -= 1

    def check_death(self):
        if self.visible and self.alive:
            if self.health <= 0:
                # Ajustar posición inicial del sprite  
                self.rect.y += 20
                #self.rect.x -= 20
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

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        original_image = pygame.image.load('./code/sprites/pieza_puz.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (TILESIZE, TILESIZE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 50)
            font_surface = self.font.render(self.text, True, BLACK)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill((190, 183, 175))

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= 0

    def up(self):
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE

class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, text, text_colour, image_path):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text
        self.text_colour = text_colour
        # Cargar y escalar la imagen de fondo para el botón
        self.background_image = pygame.image.load('./code/sprites/boton.png')
        self.background_image = pygame.transform.scale(self.background_image, (width, height))

    def draw(self, screen):
        # Dibujar la imagen de fondo del botón
        screen.blit(self.background_image, (self.x, self.y))
        
        # Dibujar el texto del botón
        font = pygame.font.SysFont("Consolas", 30)
        text_surface = font.render(self.text, True, self.text_colour)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

