import pygame
import os
from settings import LAYERS

class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, group, color, dialogue, sprite=None, interactable_type=None):
        super().__init__(group)
        self.color = color  # Guarda el color
        self.sprite = sprite  # Guarda el sprite
        self.interactable_type = interactable_type  # Guarda el tipo de interactuable

        # Configuración general
        if self.sprite is None:
            self.image = pygame.Surface((32, 32))
            self.image.fill(color)  # Usa el color pasado como argumento
        else:
            self.image = pygame.image.load(sprite).convert_alpha()  # Cargar y convertir el sprite
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['ground plant']

    def interact(self, inventory):
        print("22")
        if self.interactable_type == "trigo":
            print("24")
            inventory.añadir_trigo()
            self.kill()
        elif self.interactable_type == "madera":
            inventory.añadir_madera()
            self.kill()
        elif self.interactable_type == "dinero":
            print("31")
            inventory.añadir_dinero()
            self.kill()

    def talk(self, dialogue, inventory, personaje):
        if personaje == "don diego":
            dialogue.activar_dialogo()
            dialogue.dibujar_dialogo(inventory, "don diego")
        elif personaje == "butanero":
            dialogue.activar_dialogo()
            dialogue.dibujar_dialogo(inventory, "butanero")
            if inventory.get_dinero():
                dialogue.set_opcion_escogida(True)
            else:
                dialogue.set_opcion_escogida(True)
