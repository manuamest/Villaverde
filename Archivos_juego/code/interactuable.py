import pygame

from settings import LAYERS

class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, group, color,dialogue):
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
            self.kill()
        elif self.color == (0, 0, 255):
            inventory.añadir_madera()
            self.kill()

        elif self.color == (255,128,0):
            inventory.añadir_dinero()
            self.kill()

    def talk(self, dialogue, inventory,personaje):

        if personaje == "don diego":
            dialogue.activar_dialogo()
            dialogue.dibujar_dialogo(inventory,"don diego")
        elif personaje == "butanero":
            dialogue.activar_dialogo()
            dialogue.dibujar_dialogo(inventory,"butanero")
            if inventory.get_dinero():
                dialogue.set_opcion_escogida(True)
            else:
                dialogue.set_opcion_escogida(True)
