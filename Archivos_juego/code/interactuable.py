import pygame
from settings import *

class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Configuración general
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(500, 500))  # Posición del objeto a la derecha del jugador
        self.z = LAYERS['main']

    def interact(self):
        print("Interactuando con el objeto")