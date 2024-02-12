import pygame
from settings import *
from player import Player, InteractableObject
from sprites import *


class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        #Grupos de sprites
        self.all_sprites = CameraGroup()
        
        self.setup()


    def setup(self):
        self.player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), self.all_sprites)
        background_image = pygame.image.load('./prueba.jpg').convert_alpha()
        # Hacer el fondo 4 veces más grande
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH * 4, SCREEN_HEIGHT * 4))
        
        Generic(
            pos = (0,0),
            surf = background_image,
            groups = self.all_sprites,
            z = LAYERS['ground'])

        # Crear instancia del objeto interactuable
        InteractableObject(
            pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),  # Posición inicial del jugador
            group=self.all_sprites,color=(255,0,0))


        InteractableObject(
            pos=(SCREEN_WIDTH / 2 + 200, SCREEN_HEIGHT / 2 + 200),
            group=self.all_sprites,color=(255,255,0))

        InteractableObject(
            pos=(SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 2 + 300),
            group=self.all_sprites, color=(255, 255, 0))


        InteractableObject(
            pos=(SCREEN_WIDTH / 2 + 500, SCREEN_HEIGHT / 2 + 500),  # Posición inicial del jugador
            group=self.all_sprites,color=(0,0,255))





    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.camera = pygame.math.Vector2()

    def custom_draw(self, player):
        #Camara sigue al jugador
        self.camera.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.camera.y = player.rect.centery - SCREEN_HEIGHT / 2
        #Los sprites se dibujan por orden (ahora mismo solo hay jugador y suelo)
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.camera
                    self.display_surface.blit(sprite.image, offset_rect)
