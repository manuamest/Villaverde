import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from collections import defaultdict
from utils import import_folder, load_frames
from random import choice

class SoilTile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = LAYERS['soil water']
       
class Plant(pygame.sprite.Sprite):    
    def __init__(self, plant, groups, soil, check_watered):
        super().__init__(groups)
        self.plant = plant
        self.frames = load_frames(f'./code/sprites/plantaciones/trigo')
        self.soil = soil
        self.check_watered = check_watered
        # Parámetros de crecimiento
        self.phase = 0
        self.max_phase = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant]
        self.harvestable = False
        # sprite
        self.image = self.frames[self.phase]
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.y_offset = 70
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']
    
    def grow(self):
        #print('El método grow() se está ejecutando')
        if self.check_watered(self.rect.center):
            self.phase += self.grow_speed
            
            # Colisiones con las plantas 
            if int(self.phase) > 0:
                self.z = LAYERS['main']

            # Planta en la última fase de crecimiento
            if self.phase >= self.max_phase:
                self.phase = self.max_phase
                self.harvestable = True

            self.y_offset = -48
            self.image = self.frames[int(self.phase)]
            #self.image = pygame.transform.scale(self.image, (40, 40))
            self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))

class SoilLayer:
    def __init__(self, all_sprites):

        # Sprites
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # Cargar imagen del suelo cultivable
        self.soil_surf = pygame.image.load("./code/sprites/suelo/otoño/tile025.png")
        self.surf_water = import_folder("./code/sprites/suelo/agua")
        # Escalar la imagen del suelo al tamaño del TILE_SIZE
        self.soil_surf = pygame.transform.scale(self.soil_surf, (TILE_SIZE, TILE_SIZE))
        # Fases del trigo
        self.fases_cultivo = {  "plantar": False,
                                "sembrar": False,
                                "regar": False}

        self.create_farm_grid()
        self.create_hit_rects()

    # Establece que tiles del mapa son cultivables
    def create_farm_grid(self):
        # Obtener la capa cultivable del mapa
        cultivable_layer = load_pygame("./code/mapa/otoño/mapa_otoño.tmx").get_layer_by_name('cultivable')

        self.grid = defaultdict(lambda: defaultdict(list))

        # Llenar la matriz con los azulejos cultivables 
        for x, y, _ in cultivable_layer.tiles():
            self.grid[y][x].append('F') # el azulejo es cultivable


    def create_hit_rects(self):
        self.hit_rects = []
        # Iterar sobre la zona cultivable 
        for y in self.grid:
            for x in self.grid[y]:
                if 'F' in self.grid[y][x]:  # Solo si el Tile es cultivable
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        #print("Punto recibido:", point)
        for rect in self.hit_rects:
            # print("Rectángulo:", rect)
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                # print("Coordenadas de la cuadrícula: x =", x, ", y =", y)
                # print("Contenido de self.grid en la posición (", x, ",", y, "):", self.grid[y][x])
                if 'F' in self.grid[y][x]:
                    # print('farmable')
                    self.grid[y][x].append('C') # Tile cultivado
                    self.create_soil_tiles()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W') # Tile regado
                self.set_fase_cultivo("regar")
                WaterTile(
                    soil_sprite.rect.topleft,
                    choice(self.surf_water), 
                    [self.all_sprites, self.water_sprites])

    def check_watered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        tile = self.grid[y][x]
        is_watered = 'W' in tile      
        return is_watered
    

    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                if 'S' not in self.grid[y][x]:
                    self.grid[y][x].append('S') # Tile con una semilla plantada
                    self.set_fase_cultivo("plantar")
                    Plant(seed, [self.all_sprites, self.plant_sprites], soil_sprite, self.check_watered)
                    #print("Nueva planta creada:", new_plant)
                    #print("Tamaño del grupo de plantas:", len(self.plant_sprites.sprites()))
    
    def update_plants(self):
        #print('El método update_plants() se está ejecutando')
        for plant in self.plant_sprites.sprites():
            #print('Iterando sobre las plantas')
            plant.grow()

            
        

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        # Iterar sobre la zona cultivable solamente
        for y in self.grid:
            for x in self.grid[y]:
                if 'C' in self.grid[y][x]:  
                    SoilTile(
                        pos=(x * TILE_SIZE, y * TILE_SIZE),
                        surf=self.soil_surf,
                        groups=[self.all_sprites, self.soil_sprites]
                    )

    def set_fase_cultivo(self, fase):
        self.fases_cultivo[fase] = True
    
    def get_fase_cultivo(self, fase):
        return self.fases_cultivo[fase]
