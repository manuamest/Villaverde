import pygame
from settings import *
from timer import Timer
from inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # general setup
        self.image = pygame.Surface((32, 64))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'inventory toggle': Timer(300)  # Nuevo temporizador para el inventario
        }

        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # inventory
        self.inventory = Inventory()
        self.inventory_open = False  # Estado inicial del inventario cerrado

    def use_tool(self):
        pass
        # print(self.selected_tool)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:
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

            # tool use
            if keys[pygame.K_SPACE]:
                print(f'tool [{self.selected_tool}] is being used')
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()

            # Cambiar estado del inventario con temporizador
            if keys[pygame.K_b] and not self.timers['inventory toggle'].active:
                self.timers['inventory toggle'].activate()
                self.inventory_open = not self.inventory_open  # Cambia entre abrir y cerrar inventario

            # Acciones del inventario
            if self.inventory_open:
                self.inventory.dibujar_inventario()
                if keys[pygame.K_m]:
                    self.inventory.añadir_madera()
                if keys[pygame.K_t]:
                    self.inventory.añadir_trigo()

        # Cambiar herramienta
        if keys[pygame.K_q] and not self.timers['tool switch'].active:
            self.timers['tool switch'].activate()
            self.tool_index = (self.tool_index + 1) % len(self.tools)
            self.selected_tool = self.tools[self.tool_index]
            print(f'change tool to [{self.selected_tool}] ')

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):

        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
        
    def update(self, dt):
        self.input()
        self.update_timers()
        self.move(dt)
