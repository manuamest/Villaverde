import pygame
from settings import *
from player import Player, InteractableObject, Dialogue
from sprites import *
from overlay import Overlay
import pytmx
from inventory import Inventory
from pytmx.util_pygame import load_pygame
from soil import SoilLayer
from npc import NPC
from tutorial import Tutorial

class Level:
    def __init__(self, soil_layer, all_sprites):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.camera = pygame.math.Vector2()

        # Dialogue
        self.dialogue = Dialogue()
        self.inventory = Inventory()

        self.soil_layer = soil_layer
        self.all_sprites = all_sprites
        self.setup()
        
        # Overlay 
        self.overlay = Overlay(self.player)
        
        # Tutorial
        self.tutorial = Tutorial()
        self.tutorial.activar_tutorial()

    def setup(self):
        self.zoom = 4
        # Cargar el mapa de Tiled
        # Verano
        # self.tmx_map = load_pygame("./code/mapa/mapa_verano.tmx")
        # Otoño
        #self.tmx_map = load_pygame("./code/mapa/mapa_otoño.tmx")
        # Invierno
        self.tmx_map = load_pygame("./code/mapa/mapa_invierno2.tmx")
        # Volcán
        #self.tmx_map = load_pygame("./code/mapa/volcan.tmx")
        # Entorno pruebas
        #self.tmx_map = load_pygame("./code/mapa/pruebas2.tmx")

        #for layer in ['casa2']:
        #    for x, y, surf in self.tmx_map.get_layer_by_name(layer).tiles():
        #        Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)

        # trees 
        for obj in self.tmx_map.get_layer_by_name('arboles'):
            Tree( pos = (obj.x *5 + obj.x/10, obj.y * 7 + obj.y/2.5), surf = obj.image, groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], name = obj.name, inventory=self.inventory)

        # Obtener la capa de colisiones
        self.collision_layer = self.tmx_map.get_layer_by_name("colisiones")

        #Obtener el tamaño del mapa
        #map_width = self.tmx_map.width * self.tmx_map.tilewidth
        #map_height = self.tmx_map.height * self.tmx_map.tileheight

        #Crear el jugador en la posición deseada
        player_start_x = 3115
        player_start_y = 4600 

        self.player = Player((player_start_x, player_start_y), self.all_sprites, self.collision_layer, self.soil_layer, tree_sprites=self.tree_sprites,  inventory=self.inventory)

        #self.create_npcs()
        #self.create_objects()
        #self.create_animals()

        # Ajustar la posición y el tamaño de los objetos en el mapa
        for obj in self.collision_layer:
            obj.x *= self.zoom  # Aumentar la posición x
            obj.y *= self.zoom  # Aumentar la posición y
            obj.width *= self.zoom  # Aumentar el ancho
            obj.height *= self.zoom  # Aumentar la altura

    def create_objects(self):
        InteractableObject(
            pos=(SCREEN_WIDTH / 2 - 300, SCREEN_HEIGHT / 2 + 500),
            group=self.all_sprites, color=(255, 255, 0),dialogue=self.dialogue, sprite="./code/sprites/trigo.png", interactable_type="trigo")
        
        InteractableObject(
            pos=(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 500),
            group=self.all_sprites, color=(255, 128, 0), dialogue=self.dialogue, sprite="./code/sprites/madera.png", interactable_type="madera")
        
        InteractableObject(
            pos=(SCREEN_WIDTH / 2  - 100, SCREEN_HEIGHT / 2 + 500),
            group=self.all_sprites,color=(0,0,255),dialogue=self.dialogue, sprite="./code/sprites/dinero.png", interactable_type="dinero")
        pass

    def create_npcs(self):
        NPC(pos=(SCREEN_WIDTH / 2 + -100 , SCREEN_HEIGHT / 2 + 600),
            group=self.all_sprites, sprite_directory="./code/sprites/NPC/Don_Diego_el_VIEJO",inventory=self.inventory, dialogue=self.dialogue,personaje="don diego")
        
        NPC(pos=(SCREEN_WIDTH / 2 - 300 , SCREEN_HEIGHT / 2 + 600),
            group=self.all_sprites, sprite_directory="./code/sprites/NPC/Jordi_el_obrero",inventory=self.inventory, dialogue=self.dialogue,personaje="butanero")
        
        NPC(pos=(SCREEN_WIDTH / 2 + 500 , SCREEN_HEIGHT / 2 + 1500),
            group=self.all_sprites, sprite_directory="./code/sprites/NPC/Eva_la_modista",inventory=self.inventory, dialogue=self.dialogue,personaje="modista")
        
        NPC(pos=(SCREEN_WIDTH / 2 + 500 , SCREEN_HEIGHT / 2 + 1700),
            group=self.all_sprites, sprite_directory="./code/sprites/NPC/Xoel_el_tendero",inventory=self.inventory, dialogue=self.dialogue,personaje="mercader")
        pass

    def create_animals(self):
        NPC(pos=(SCREEN_WIDTH / 2 - 300 , SCREEN_HEIGHT / 2 - 300),
            group=self.all_sprites, sprite_directory="./code/sprites/animales/cabra",inventory=self.inventory, dialogue=self.dialogue,personaje="mercader")

        NPC(pos=(SCREEN_WIDTH / 2  , SCREEN_HEIGHT / 2 - 300),
            group=self.all_sprites, sprite_directory="./code/sprites/animales/vaca_blanca",inventory=self.inventory, dialogue=self.dialogue,personaje="mercader")

        NPC(pos=(SCREEN_WIDTH / 2 + 300 , SCREEN_HEIGHT / 2 - 300),
            group=self.all_sprites, sprite_directory="./code/sprites/animales/oveja",inventory=self.inventory, dialogue=self.dialogue,personaje="mercader")

        NPC(pos=(SCREEN_WIDTH / 2 + 500 , SCREEN_HEIGHT / 2 - 300),
            group=self.all_sprites, sprite_directory="./code/sprites/animales/pollo",inventory=self.inventory, dialogue=self.dialogue,personaje="mercader")

    def run(self, dt):
        self.display_surface.fill('black')

        # Centrar la cámara en el jugador
        self.camera.x = self.player.rect.centerx - SCREEN_WIDTH / 2
        self.camera.y = self.player.rect.centery - SCREEN_HEIGHT / 2

        # Dibujar el fondo desde el mapa de Tiled
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        # Ajustar el tamaño de la imagen del fondo
                        scaled_tile = pygame.transform.scale(tile, (int(tile.get_width() * self.zoom), int(tile.get_height() * self.zoom)))
                        self.display_surface.blit(scaled_tile, (x * self.tmx_map.tilewidth * self.zoom - self.camera.x,
                                                                y * self.tmx_map.tileheight * self.zoom - self.camera.y))

        self.all_sprites.custom_draw(self.player, self.zoom, self.tree_sprites)
        self.all_sprites.update(dt)
        self.plant_collision()

        # Mover al jugador
        self.player.move(dt)

        # Para mostrar el overlay
        self.overlay.display()
        
        # Tutorial
        #self.tutorial.mostrar_tutorial()
        
    def check_collision(self):
        player_rect = self.player.rect

        # Verificar colisiones en la capa de colisiones del mapa de Tiled
        for obj in self.collision_layer:
            col_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if player_rect.colliderect(col_rect):
                # Detener al jugador ante la colisión
                self.player.stop()

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.rect):
                    # Añadir una unidad de trigo al inventario
                    self.player.inventory.añadir_trigo()
                    plant.kill()
                    #Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
                    # Coordenadas del tile
                    x = plant.rect.centerx // TILE_SIZE
                    y = plant.rect.centery // TILE_SIZE
                    if 'S' in self.soil_layer.grid[y][x]:
                        self.soil_layer.grid[y][x].remove('S')
                    if 'W' in self.soil_layer.grid[y][x]:
                        self.soil_layer.grid[y][x].remove('W')
                        # Eliminar el agua del tile
                        for water_sprite in self.soil_layer.water_sprites.sprites():
                            if water_sprite.rect.collidepoint((x * TILE_SIZE, y * TILE_SIZE)):
                                water_sprite.kill()
                
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.camera = pygame.math.Vector2()

    def custom_draw(self, player, zoom, tree_sprites):
        # Cámara sigue al jugador
        self.camera.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.camera.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == 7:
                    scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width) * zoom, int(sprite.rect.height) * zoom))
                elif sprite.z == 6:
                    scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width) / zoom, int(sprite.rect.height) / zoom))
                else:
                    scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width), int(sprite.rect.height)))
                    
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    
                    if sprite in tree_sprites:
                        # Ajustar la posición del árbol para dibujar correctamente
                        offset_rect.centery -= sprite.rect.height * 0.9
                        scaled_rect = scaled_image.get_rect(center=(offset_rect.centerx - self.camera.x, offset_rect.centery - self.camera.y))
                    else:
                        offset_rect.center -= self.camera
                        scaled_rect = scaled_image.get_rect(center=offset_rect.center)
                    self.display_surface.blit(scaled_image, scaled_rect.topleft)
