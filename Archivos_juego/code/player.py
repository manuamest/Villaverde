import pygame
from settings import *
from timer import Timer
from inventory import Inventory
from interactuable import InteractableObject
from utils import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_layer):
        super().__init__(group)

        self.import_assets()
        self.frame_index = 0
        self.status = 'abajo'

        self.collision_layer = collision_layer
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 120

        self.timers = {
            'uso de herramienta': Timer(350, self.use_tool),
            'cambio de herramienta': Timer(200),
            'alternar inventario': Timer(1000),
            'interacción': Timer(300)
        }

        # Tamaño original del jugador
        self.original_width = self.rect.width
        self.original_height = self.rect.height

        self.tools = ['azada', 'hacha', 'agua']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        self.inventory = Inventory()
        self.inventario_abierto = False

    def use_tool(self):
        if self.selected_tool == 'azada':
            pass
		
        if self.selected_tool == 'hacha':
            pass
		
        if self.selected_tool == 'agua':
            pass

    def import_assets(self):
        self.animations = {'arriba': [], 'abajo': [], 'izquierda': [], 'derecha': [],
                        'derecha_inactivo': [], 'izquierda_inactivo': [], 'arriba_inactivo': [], 'abajo_inactivo': [],
                        'derecha_azada': [], 'izquierda_azada': [], 'arriba_azada': [], 'abajo_azada': [],
                        'derecha_hacha': [], 'izquierda_hacha': [], 'arriba_hacha': [], 'abajo_hacha': [],
                        'derecha_agua': [], 'izquierda_agua': [], 'arriba_agua': [], 'abajo_agua': []}

        for animation in self.animations.keys():
            full_path = 'code/sprites/wuan/' + animation
            self.animations[animation] = import_folder(full_path)


    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]


    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['uso de herramienta'].active:
            self.direction = pygame.math.Vector2(0, 0)  # Reiniciar la dirección

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'arriba'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'abajo'

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'derecha'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'izquierda'

            if keys[pygame.K_SPACE]:
                print(f'Herramienta [{self.selected_tool}] está siendo usada')
                self.timers['uso de herramienta'].activate()
                self.frame_index = 0

            if keys[pygame.K_b] and not self.timers['alternar inventario'].active:
                self.timers['alternar inventario'].activate()
                self.inventario_abierto = not self.inventario_abierto

            if self.inventario_abierto:
                self.inventory.dibujar_inventario()

            if keys[pygame.K_q] and not self.timers['cambio de herramienta'].active:
                self.timers['cambio de herramienta'].activate()
                self.tool_index = (self.tool_index + 1) % len(self.tools)
                self.selected_tool = self.tools[self.tool_index]
                print(f'Cambiando a herramienta [{self.selected_tool}] ')

            if keys[pygame.K_e] and not self.timers['interacción'].active:
                self.timers['interacción'].activate()
                player_center = pygame.math.Vector2(self.rect.center)
                for sprite in self.groups()[0].sprites():
                    if isinstance(sprite, InteractableObject):
                        obj_center = pygame.math.Vector2(sprite.rect.center)
                        distancia = player_center.distance_to(obj_center)
                        if distancia < 50:
                            sprite.interact(self.inventory)

    def get_status(self):
        # Si no hay movimiento (está en reposo)
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_inactivo'

        # Si está utilizando una herramienta
        if self.timers['uso de herramienta'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def stop(self):
        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = -self.direction

    def move(self, dt):
        new_pos = self.pos + self.velocity * dt
        new_rect = self.rect.copy()
        new_rect.center = new_pos

        # Check for collisions before updating the position
        if not self.check_collision(new_rect):
            self.pos = new_pos
            self.rect.center = self.pos

    def check_collision(self, new_rect):
        # Check for collisions in the collision layer
        for obj in self.collision_layer:
            col_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if new_rect.colliderect(col_rect):
                # Collision detected, return True
                return True

        # No collision detected, return False
        return False

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.velocity = self.direction * self.speed  # Actualizar la velocidad basada en la dirección
        self.move(dt)
        self.animate(dt)