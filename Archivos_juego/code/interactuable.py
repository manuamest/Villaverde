import pygame
import os
from settings import LAYERS

class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, group, color, dialogue, sprite=None, interactable_type=None, location="fuera"):
        super().__init__(group)
        self.location = location
        self.color = color  # Guarda el color
        self.sprite = sprite  # Guarda el sprite
        self.interactable_type = interactable_type  # Guarda el tipo de interactuable
        self.visible = True
        if location=="fuera":
            self.visible == True
        else:
            self.visible == False
        # Configuración general
        if self.sprite is None:
            self.image = pygame.Surface((32, 32))
            self.image.fill(color)  # Usa el color pasado como argumento
        else:
            self.image = pygame.image.load(sprite).convert_alpha()  # Cargar y convertir el sprite

        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['ground plant']

    def interact(self, inventory):
        if self.visible == True:
            if self.interactable_type == "trigo":
                inventory.añadir_trigo()
                self.kill()
            elif self.interactable_type == "madera":
                inventory.añadir_madera()
                self.kill()
            elif self.interactable_type == "dinero":
                inventory.añadir_dinero()
                self.kill()

    def make_invisible(self, location):
        if self.location != location:
            self.visible = False
            self.image = pygame.image.load('code/sprites/invisible.png')
        else:
            self.visible = True
            self.image = self.original_image
