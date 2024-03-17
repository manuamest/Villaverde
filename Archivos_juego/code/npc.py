import pygame
import os

from settings import LAYERS

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, group, sprite_directory,inventory,dialogue,draw, personaje, location):
        super().__init__(group)
        self.sprite_directory = sprite_directory
        self.dialogue = dialogue
        self.draw = draw
        self.location = location

        # Cargar sprites
        self.sprites = self.load_sprites()
        self.original_sprites = self.sprites
        self.dialogo_abierto = False 

        # Configuración inicial
        self.image = self.sprites[0]  
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # Variables de animación
        self.current_frame = 0
        self.animation_delay = 13
        self.animation_counter = 0

        self.personaje = personaje 

        self.visible = True
        self.make_invisible("fuera")

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
        if self.visible == True:
            if personaje == "don diego":
                dialogue.set_opcion_dialogo(True)
                self.draw.dibujar_dialogo(inventory, "don diego")
            elif personaje == "mercader":
                dialogue.set_opcion_dialogo(True)
                self.draw.dibujar_dialogo(inventory,"mercader")
            elif personaje == "modista":
                dialogue.set_opcion_dialogo(True)
                self.draw.dibujar_dialogo(inventory,"modista")
            elif personaje == "obrero":
                dialogue.set_opcion_dialogo(True)
                self.draw.dibujar_dialogo(inventory, "obrero")
            elif personaje == "hermanos":
                dialogue.set_opcion_dialogo(True)
                self.draw.dibujar_dialogo(inventory, "hermanos")

    def make_invisible(self, location):
        if self.location != location:
            self.visible = False
            for i in range(len(self.sprites)):
                self.sprites[i] = pygame.image.load('code/sprites/invisible.png')
        else:
            self.visible = True
            self.sprites = self.load_sprites()
                    
    def update(self, dt):
        self.update_animation()
          
                    
    def update(self, dt):
        self.update_animation()
