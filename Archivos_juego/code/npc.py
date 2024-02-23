import pygame
import os

from settings import LAYERS

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, group, sprite_directory,inventory,dialogue, personaje):
        super().__init__(group)
        self.sprite_directory = sprite_directory
        self.dialogue = dialogue

        # Load sprite images
        self.sprites = self.load_sprites()
        self.dialogo_abierto = False 
       

        # Configuración inicial
        self.image = self.sprites[0]  # Use the first sprite as the initial image
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['npc']

        # Animation variables
        self.current_frame = 0
        self.animation_delay = 5
        self.animation_counter = 0

        self.personaje= personaje 

    def load_sprites(self):
        sprites = []
        for filename in os.listdir(self.sprite_directory):
            path = os.path.join(self.sprite_directory, filename)
            sprites.append(pygame.image.load(path).convert_alpha())
        return sprites

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
            self.image = self.sprites[self.current_frame]

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
