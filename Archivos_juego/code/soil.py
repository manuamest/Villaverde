import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilTile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = LAYERS['soil']

class SoilLayer:
    def __init__(self, all_sprites):
        # Sprites
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # Cargar imagen del suelo cultivable
        self.soil_surf = pygame.image.load("./code/sprites/suelo/otoño/tile025.png")
        # Escalar la imagen del suelo al tamaño del TILE_SIZE
        self.soil_surf = pygame.transform.scale(self.soil_surf, (TILE_SIZE, TILE_SIZE))

        self.create_farm_grid()
        self.create_hit_rects()

    # Establece que tiles del mapa son cultivables
    def create_farm_grid(self):
        h_tiles, v_tiles = 40, 80

        self.grid = [[[] for col in range(h_tiles)] for row in range (v_tiles)]
        for x, y, _ in load_pygame("./code/mapa/mapa_otoño.tmx").get_layer_by_name('cultivable').tiles():
            self.grid[y][x].append('C')
        #print(self.grid)


    def create_hit_rects(self):
        self.hit_rects = []
        for row_ind , row in enumerate(self.grid):
            for col_ind, tile in enumerate(row):
                if 'C' in tile:
                    x = col_ind * TILE_SIZE 
                    y = row_ind * TILE_SIZE 
                    rect = pygame.Rect(x,y,TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        print("Punto recibido:", point)
        for rect in self.hit_rects:
            #print("Rectángulo:", rect)
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                print("Coordenadas de la cuadrícula: x =", x, ", y =", y)
                print("Contenido de self.grid en la posición (", x, ",", y, "):", self.grid[y][x])
                if 'C' in self.grid[y][x]:
                    print('farmable')
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                    print(self.grid)

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for row_ind, row in enumerate(self.grid):
            for col_ind, tile in enumerate(row):
                if 'X' in tile:
                    SoilTile(
                        pos = (col_ind * TILE_SIZE, row_ind * TILE_SIZE), 
						surf = self.soil_surf, 
						groups = [self.all_sprites, self.soil_sprites])


