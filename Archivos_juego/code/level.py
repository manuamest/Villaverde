import pygame
from settings import *
from player import Player


class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        #Grupos de sprites
        self.all_sprites = pygame.sprite.Group()

        #Posicion de la camara
        self.camera = pygame.math.Vector2(0, 0)

        #Cargar la imagen de fondo
        self.background = pygame.image.load('./prueba.jpg').convert()

        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)

    def update_camera(self):
        #Hacer que la cámara siga al jugador
        self.camera.x = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera.y = self.player.rect.centery - SCREEN_HEIGHT // 2

    def run(self, dt):
        self.update_camera()

        #Dibujar el fondo
        self.display_surface.blit(self.background, (0 - self.camera.x, 0 - self.camera.y))

        #Dibujar los sprites
        for sprite in self.all_sprites:
            self.display_surface.blit(sprite.image, sprite.rect.move(-self.camera.x, -self.camera.y))

        #Actualizar todos los sprites
        self.all_sprites.update(dt)