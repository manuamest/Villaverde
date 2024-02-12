import pygame

from Archivos_juego.code.settings import LAYERS


class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, group, color):
        super().__init__(group)
        self.color = color  # Guarda el color

        # Configuración general
        self.image = pygame.Surface((32, 32))
        self.image.fill(color)  # Usa el color pasado como argumento
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

    def interact(self, inventory):

        if self.color == (255, 255, 0):
            inventory.añadir_trigo()
            print("Añadido trigo al inventario")
            self.kill()
        elif self.color == (0, 0, 255):
            inventory.añadir_madera()
            print("Añadida madera al inventario")
            self.kill()

        else:
            print("Interactuando con jugador")
