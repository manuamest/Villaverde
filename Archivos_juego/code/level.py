import pygame
from settings import *
from player import Player, InteractableObject
from sprites import *
from overlay import Overlay

import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from settings import *

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.camera = pygame.math.Vector2()
        self.setup()
        
        # Overlay 
        self.overlay = Overlay(self.player)

    def setup(self):
        # Cargar el mapa de Tiled
        self.tmx_map = load_pygame("./code/mapa/mapa.tmx")

        # Obtener la capa de colisiones
        self.collision_layer = self.tmx_map.get_layer_by_name("colisiones")

        # Obtener el tamaño del mapa
        map_width = self.tmx_map.width * self.tmx_map.tilewidth
        map_height = self.tmx_map.height * self.tmx_map.tileheight

        # Crear el jugador en el centro del mapa
        player_start_x = map_width / 2
        player_start_y = map_height / 2

        # Reducir el tamaño del jugador
        player_size = (8, 16)
        self.player = Player((player_start_x, player_start_y), self.all_sprites, self.collision_layer, size=player_size)
        self.player.z = (LAYERS['main'] + LAYERS['main']+1) / 2  # Establecer z del jugador entre la primera y última capa

        # Crear instancias de objetos interactuables
        InteractableObject(
            pos=(player_start_x, player_start_y),  # Posición inicial del jugador
            group=self.all_sprites, color=(255, 0, 0))

        InteractableObject(
            pos=(player_start_x + 200, player_start_y + 200),
            group=self.all_sprites, color=(255, 255, 0))

        InteractableObject(
            pos=(player_start_x + 300, player_start_y + 300),
            group=self.all_sprites, color=(255, 255, 0))

        InteractableObject(
            pos=(player_start_x + 500, player_start_y + 500),  # Posición inicial del jugador
            group=self.all_sprites, color=(0, 0, 255))

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
                        self.display_surface.blit(tile, (x * self.tmx_map.tilewidth - self.camera.x,
                                                        y * self.tmx_map.tileheight - self.camera.y))

        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        # Verificar colisiones
        self.check_collision()

        # Mover al jugador
        self.player.move(dt)

        # Para mostrar el overlay
        self.overlay.display()

    def draw_tiled_map(self):
        # Dibujar el fondo desde el mapa de Tiled
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        self.display_surface.blit(tile, (x * self.tmx_map.tilewidth - self.camera.x,
                                                        y * self.tmx_map.tileheight - self.camera.y))

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

    def custom_draw(self, player):
        # Camara sigue al jugador
        self.camera.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.camera.y = player.rect.centery - SCREEN_HEIGHT / 2

        # Obtener todos los sprites, excepto el jugador
        sprites_without_player = [sprite for sprite in self.sprites() if sprite != player]

        # Sortear sprites basados en su atributo z
        sprites_sorted = sorted(sprites_without_player, key=lambda sprite: sprite.z)

        # Dibujar sprites antes de la primera capa
        for layer in range(LAYERS['main']):
            for sprite in sprites_sorted:
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.camera
                    self.display_surface.blit(sprite.image, offset_rect)

        # Dibujar al jugador entre la primera capa y el resto
        offset_rect = player.rect.copy()
        offset_rect.center -= self.camera
        self.display_surface.blit(player.image, offset_rect)

        # Dibujar sprites después de la primera capa
        for layer in range(LAYERS['main'] + 1, len(LAYERS)):
            for sprite in sprites_sorted:
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.camera
                    self.display_surface.blit(sprite.image, offset_rect)