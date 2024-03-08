import pygame
import os
import random

from settings import LAYERS

class Animal(pygame.sprite.Sprite):
    def __init__(self, pos, group, animal_type, inventory, dialogue, personaje, prime=False, walk=4,location="fuera"):
        super().__init__(group)
        self.animal_type = animal_type
        self.sprite_directory = os.path.join("./code/sprites/animales/", animal_type)
        self.dialogue = dialogue
        self.prime = prime
        self.location = location
        self.visible = True
        if location=="fuera":
            self.visible == True
        else:
            self.visible == False
        # Load sprite images for walking and inactive states
        if self.prime:  # Comprueba si está en estado cabraprime
            self.sprites_caminando = self.load_sprites(os.path.join(self.sprite_directory, f"{animal_type}_caminando_prime"))
            self.sprites_inactivo = self.load_sprites(os.path.join(self.sprite_directory, f"{animal_type}_inactivo_prime"))
        else:
            self.sprites_caminando = self.load_sprites(os.path.join(self.sprite_directory, f"{animal_type}_caminando"))
            self.sprites_inactivo = self.load_sprites(os.path.join(self.sprite_directory, f"{animal_type}_inactivo"))
        self.dialogo_abierto = False 
        
        # Configuración inicial
        self.image = self.sprites_inactivo[0]  # Use the first sprite as the initial image
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # Animation variables
        self.current_frame = 0
        self.animation_delay = 13
        self.animation_counter = 0

        # Additional states
        self.state = "inactivo"  # Default state
        self.personaje = personaje 

        self.move_index = 0
        self.move_speed = 2  # Velocidad de movimiento
        self.stop_duration = 60  # Duración de la parada en cada posición, en número de actualizaciones
        self.stop_counter = 0  # Contador para rastrear la duración de la parada
        self.direction = 1  # Dirección inicial: 1 para derecha, -1 para izquierda

        # Movement variables based on 'walk' parameter
        if walk == 0:  # Cabra
            self.move_speed = 3
            self.target_positions = [(pos[0] + 50, pos[1] + 50), (pos[0] - 50, pos[1] - 50)]
        elif walk == 1:  # Pollo
            self.move_speed = 1
            self.stop_duration = 100
            self.target_positions = [(pos[0] - 200, pos[1] - 60), (pos[0] + 10, pos[1] - 30)]
        elif walk == 2:  # Vaca
            self.move_speed = 1
            self.stop_duration = 200
            self.target_positions = [(pos[0] + 100, pos[1] + 100), (pos[0] - 100, pos[1] - 100)]
        elif walk == 3:  # Oveja
            self.move_speed = 2
            self.target_positions = [(pos[0] + 30, pos[1] + 30), (pos[0] - 30, pos[1] - 30)]
        else:  # Predeterminado para otros animales
            self.move_speed = 2
            self.target_positions = [(pos[0] - 200, pos[1] - 60), (pos[0] + 10, pos[1] - 30)]

    def load_sprites(self, directory):
        sprites = []
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            sprites.append(pygame.image.load(path).convert_alpha())
        return sprites

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0
            if self.state == "caminando":
                self.current_frame = (self.current_frame + 1) % len(self.sprites_caminando)
                if self.direction == -1:  # Si la dirección es hacia la izquierda, reflejar horizontalmente el sprite
                    self.image = pygame.transform.flip(self.sprites_caminando[self.current_frame], True, False)
                else:
                    self.image = self.sprites_caminando[self.current_frame]
            elif self.state == "inactivo":
                self.current_frame = (self.current_frame + 1) % len(self.sprites_inactivo)
                if self.direction == -1:  # Si la dirección es hacia la izquierda, reflejar horizontalmente el sprite
                    self.image = pygame.transform.flip(self.sprites_inactivo[self.current_frame], True, False)
                else:
                    self.image = self.sprites_inactivo[self.current_frame]

    def set_state(self, state):
        self.state = state

    def talk_animal(self, dialogue, inventory, personaje):
        if self.visible == True:
            self.set_state("inactivo")
            self.stop_counter = 20
            if personaje == "pollo":
                dialogue.set_opcion_dialogo(True)
                dialogue.dibujar_dialogo(inventory, "pollo")
            elif personaje == "oveja":
                dialogue.set_opcion_dialogo(True)
                dialogue.dibujar_dialogo(inventory, "oveja")     
            elif personaje == "vaca":
                dialogue.set_opcion_dialogo(True)
                dialogue.dibujar_dialogo(inventory, "vaca")

          
    def update(self, dt):
        if self.state == "inactivo":
            self.update_animation()
            # Incrementar el contador de parada
            self.stop_counter += 1
            if self.stop_counter >= self.stop_duration:
                self.stop_counter = 0
                # Cambiar a estado caminando
                self.set_state("caminando")
        elif self.state == "caminando":
            self.update_animation()
            # Obtener la posición objetivo actual
            target_pos = self.target_positions[self.move_index]
            # Calcular la dirección hacia la posición objetivo
            dx = target_pos[0] - self.rect.centerx
            dy = target_pos[1] - self.rect.centery
            # Calcular la distancia total al objetivo
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            # Normalizar la dirección y escalarla por la velocidad
            dx /= distance
            dy /= distance
            dx *= self.move_speed
            dy *= self.move_speed
            # Mover hacia la posición objetivo
            self.rect.centerx += dx
            self.rect.centery += dy
            # Comprobar si la cabra ha alcanzado la posición objetivo
            if abs(self.rect.centerx - target_pos[0]) < self.move_speed and abs(self.rect.centery - target_pos[1]) < self.move_speed:
                # La cabra ha alcanzado la posición objetivo, cambiar a estado inactivo
                self.set_state("inactivo")
                # Reiniciar el contador de parada
                self.stop_counter = 0
                # Incrementar el índice de movimiento
                self.move_index = (self.move_index + 1) % len(self.target_positions)
                # Cambiar la dirección si la nueva posición es hacia la izquierda
                if self.target_positions[self.move_index][0] < self.rect.centerx:
                    self.direction = -1
                else:
                    self.direction = 1
    
    def make_invisible(self, location):
        if self.location != location:
            self.visible = False
            for i in range(len(self.sprites_caminando)):
                self.sprites_caminando[i] = pygame.image.load('code/sprites/invisible.png')
            for i in range(len(self.sprites_inactivo)):
                self.sprites_inactivo[i] = pygame.image.load('code/sprites/invisible.png')
        else:
            self.visible = True
            if self.prime:  # Comprueba si está en estado cabraprime
                self.sprites_caminando = self.load_sprites(os.path.join(self.sprite_directory, f"{self.animal_type}_caminando_prime"))
                self.sprites_inactivo = self.load_sprites(os.path.join(self.sprite_directory, f"{self.animal_type}_inactivo_prime"))
            else:
                self.sprites_caminando = self.load_sprites(os.path.join(self.sprite_directory, f"{self.animal_type}_caminando"))
                self.sprites_inactivo = self.load_sprites(os.path.join(self.sprite_directory, f"{self.animal_type}_inactivo"))
