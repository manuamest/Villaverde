import pygame
from settings import *
from timer import Timer
from inventory import Inventory
from interactuable import InteractableObject

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Configuración general
        self.image = pygame.Surface((32, 64))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # Atributos de movimiento
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Temporizadores
        self.timers = {
            'uso de herramienta': Timer(350, self.use_tool),
            'cambio de herramienta': Timer(200),
            'alternar inventario': Timer(1000),  # Temporizador para el inventario
            'interacción': Timer(300)  # Temporizador para la interacción con objetos
        }

        # Herramientas
        self.tools = ['azada', 'hacha', 'agua']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Inventario
        self.inventory = Inventory()
        self.inventario_abierto = False  # Estado inicial del inventario cerrado

    def use_tool(self):
        pass
        # print(self.selected_tool)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['uso de herramienta'].active:
            if keys[pygame.K_w]:
                self.direction.y = -1
            elif keys[pygame.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
            elif keys[pygame.K_a]:
                self.direction.x = -1
            else:
                self.direction.x = 0

            # Uso de herramienta
            if keys[pygame.K_SPACE]:
                print(f'Herramienta [{self.selected_tool}] está siendo usada')
                self.timers['uso de herramienta'].activate()
                self.direction = pygame.math.Vector2()

            # Alternar estado del inventario
            if keys[pygame.K_b] and not self.timers['alternar inventario'].active:
                self.timers['alternar inventario'].activate()
                self.inventario_abierto = not self.inventario_abierto  # Cambia entre abrir y cerrar inventario

            # Acciones del inventario
            if self.inventario_abierto:
                self.inventory.dibujar_inventario()

            # Cambiar herramienta
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
                        if distancia < 50:  # Si está lo suficientemente cerca para interactuar
                            sprite.interact(self.inventory)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):

        # Normalizar un vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Movimiento horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Movimiento vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.update_timers()
        self.move(dt)
