import pygame
from settings import *
from player import Player, InteractableObject, Dialogue
from sprites import *
from overlay import Overlay
import pytmx
from pytmx.util_pygame import load_pygame
from soil import SoilLayer

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.camera = pygame.math.Vector2()

        # Dialogue
        self.dialogue = Dialogue()

        self.soil_layer = SoilLayer(self.all_sprites)
        self.setup()
        
        # Overlay 
        self.overlay = Overlay(self.player)


        

    def setup(self):
        self.zoom = 4
        # Cargar el mapa de Tiled
        # Verano
        self.tmx_map = load_pygame("./code/mapa/mapa_verano.tmx")
        # Otoño
        #self.tmx_map = load_pygame("./code/mapa/mapa_otoño.tmx")
        # Invierno
        # self.tmx_map = load_pygame("./code/mapa/mapa_invierno.tmx")
        # Volcán
        #self.tmx_map = load_pygame("./code/mapa/volcan.tmx")

        # Obtener la capa de colisiones
        self.collision_layer = self.tmx_map.get_layer_by_name("colisiones")

        # Obtener el tamaño del mapa
        map_width = self.tmx_map.width * self.tmx_map.tilewidth
        map_height = self.tmx_map.height * self.tmx_map.tileheight

        # Crear el jugador en el centro del mapa
        player_start_x = map_width / 2
        player_start_y = map_height / 2

        self.player = Player((player_start_x, player_start_y), self.all_sprites, self.collision_layer, self.soil_layer)

        # Crear instancias de objetos interactuables
        InteractableObject(
            pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),  # Posición inicial del jugador
            group=self.all_sprites,color=(255,0,0),dialogue=self.dialogue)


        InteractableObject(
            pos=(SCREEN_WIDTH / 2 + 200, SCREEN_HEIGHT / 2 + 200),
            group=self.all_sprites,color=(255,255,0),dialogue=self.dialogue)

        InteractableObject(
            pos=(SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 2 + 300),
            group=self.all_sprites, color=(255, 255, 0),dialogue=self.dialogue)

        InteractableObject(
            pos=(SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 2 + 500),
            group=self.all_sprites, color=(255, 128, 0), dialogue=self.dialogue)


        InteractableObject(
            pos=(SCREEN_WIDTH / 2 + 500, SCREEN_HEIGHT / 2 + 500),  # Posición inicial del jugador
            group=self.all_sprites,color=(0,0,255),dialogue=self.dialogue)

        InteractableObject(
            pos=(SCREEN_WIDTH / 2 + 600, SCREEN_HEIGHT / 2 + 600),  # Posición inicial del jugador
            group=self.all_sprites, color=(255, 0, 255), dialogue=self.dialogue)

        
        # Ajustar la posición y el tamaño de los objetos en el mapa
        for obj in self.collision_layer:
            obj.x *= self.zoom  # Aumentar la posición x
            obj.y *= self.zoom  # Aumentar la posición y
            obj.width *= self.zoom  # Aumentar el ancho
            obj.height *= self.zoom  # Aumentar la altura

        # trees 
        #for obj in tmx_data.get_layer_by_name('Trees'): 
        #    Tree( pos = (obj.x, obj.y), surf = obj.image, groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], name = obj.name, player_add = self.player_add)

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


        self.all_sprites.custom_draw(self.player, self.zoom)
        self.all_sprites.update(dt)

        # Verificar colisiones
        self.check_collision()

        # Mover al jugador
        self.player.move(dt)

        # Para mostrar el overlay
        self.overlay.display()

    def check_collision(self):
        player_rect = self.player.rect

        # Verificar colisiones en la capa de colisiones del mapa de Tiled
        for obj in self.collision_layer:
            col_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if player_rect.colliderect(col_rect):
                # Detener al jugador ante la colisión
                self.player.stop()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.camera = pygame.math.Vector2()

    def custom_draw(self, player, zoom):
        # Camara sigue al jugador
        self.camera.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.camera.y = player.rect.centery - SCREEN_HEIGHT / 2

        # Obtener todos los sprites, excepto el jugador
        sprites_without_player = [sprite for sprite in self.sprites() if sprite != player]

        # Sortear sprites basados en su atributo z
        sprites_sorted = sorted(sprites_without_player, key=lambda sprite: sprite.z)

        # Dibujar sprites antes de la primera capa
        for layer in range(LAYERS['main']):
                    # Dibujar los sprites
            for sprite in sprites_sorted:
                offset_rect = sprite.rect.copy()
                offset_rect.center -= self.camera
                scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width), int(sprite.rect.height)))
                self.display_surface.blit(scaled_image, offset_rect)

        # Dibujar al jugador
        offset_rect = player.rect.copy()
        offset_rect.center -= self.camera
        scaled_image = pygame.transform.scale(player.image, (int(player.image.get_width() * zoom), int(player.image.get_height() * zoom)))
        scaled_rect = scaled_image.get_rect(center=offset_rect.center)
        self.display_surface.blit(scaled_image, scaled_rect.topleft)


        # Dibujar sprites después de la primera capa
        for layer in range(LAYERS['main'] + 1, len(LAYERS)):
            for sprite in sprites_sorted:
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.camera
                    self.display_surface.blit(sprite.image, offset_rect)
