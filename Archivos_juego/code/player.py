import pygame
from settings import *
from timer import Timer
from dialogue import Dialogue
from inventory import Inventory
from interactuable import InteractableObject
from npc import NPC
from animals import Animal
from utils import import_folder
from puzle import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_layer, soil_layer, director, tree_sprites, inventory, level, dialogue, draw):
        super().__init__(group)

        self.import_assets()
        self.frame_index = 0
        self.status = 'abajo'

        self.inventory = inventory
        self.draw = draw

        self.collision_layer = collision_layer
        self.soil_layer = soil_layer
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100

        self.puzle = Puzle(self.inventory.screen)

        self.level = level
        self.director = director

        # Diálogo
        self.dialogue = dialogue
        self.personaje_actual = None

        self.timers = {
            'uso de herramienta': Timer(350, self.use_tool),
            'uso de semilla': Timer(350, self.use_seed),
            'cambio de herramienta': Timer(200),
            'alternar inventario': Timer(200),
            'interaccion': Timer(300),
            'dialogo': Timer(1000)
        }

        # Tamaño original del jugador
        self.original_width = self.rect.width
        self.original_height = self.rect.height

        # Herramientas
        self.tools = ['azada', 'hacha', 'agua']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Semillas
        self.seed = ['trigo']
        self.seed_index = 0
        self.selected_seed = self.seed[self.seed_index]
     
        self.tree_sprites = tree_sprites
        self.cut_down_tree = False
        self.talk_with_list = { "don diego": False,
                                "mercader": False,
                                "modista": False,
                                "butanero": False,
                                "cabra": False,
                                "oveja": False,
                                "pollo": False,
                                "vaca marron": False}
        self.inventario_abierto = False
        self.interact_last_object = False

    def use_tool(self):
        if self.selected_tool == 'azada':
            if self.level.escene == "Nivel2":
                self.soil_layer.get_hit(self.target_pos)
        
        if self.selected_tool == 'hacha':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos) and tree.alive:
                    tree.damage()
                    self.cut_down_tree = True

        if self.selected_tool == 'agua':
            if self.level.escene == "Nivel2":
                self.soil_layer.water(self.target_pos)

    def use_seed(self):
        if self.level.escene == "Nivel2":
            self.soil_layer.plant_seed(self.target_pos, self.selected_seed)

    def get_target_pos(self):
        # Obtén la posición del jugador en coordenadas de tiles
        player_tile_x = self.rect.centerx // TILE_SIZE
        player_tile_y = self.rect.centery // TILE_SIZE
        
        # Calcula la posición del objetivo basada en las coordenadas de tiles
        target_tile_pos = (player_tile_x, player_tile_y)
        
        # Multiplica la posición del tile por el tamaño del tile para obtener la posición en píxeles
        self.target_pos = (target_tile_pos[0] * TILE_SIZE, target_tile_pos[1] * TILE_SIZE)

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

            if keys[pygame.K_f] and not self.dialogue.obtener_dialogo():
                self.timers['uso de semilla'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_TAB] and not self.timers['alternar inventario'].active and not self.dialogue.obtener_dialogo():
                self.timers['alternar inventario'].activate()
                self.inventario_abierto = not self.inventario_abierto

            if self.inventario_abierto:
                self.inventory.dibujar_inventario()
            elif keys[pygame.K_SPACE] and not self.dialogue.obtener_dialogo():
                self.timers['uso de herramienta'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
            
            if self.dialogue.obtener_dialogo():
                self.draw.dibujar_dialogo(self.inventory, self.personaje_actual)
                dialogos_personaje = self.dialogue.obtener_dialogo_personaje(self.personaje_actual)
                self.draw.procesar_dialogo(keys, dialogos_personaje,self.timers,self.personaje_actual)

            if keys[pygame.K_q] and not self.timers['cambio de herramienta'].active and not self.dialogue.obtener_dialogo():
                self.timers['cambio de herramienta'].activate()
                self.tool_index = (self.tool_index + 1) % len(self.tools)
                self.selected_tool = self.tools[self.tool_index]
  
            if keys[pygame.K_e] and not self.timers['interaccion'].active:
                self.timers['interaccion'].activate()
                player_center = pygame.math.Vector2(self.rect.center)
                for sprite in self.groups()[0].sprites():
                    if (isinstance(sprite, InteractableObject) or isinstance(sprite, NPC) or isinstance(sprite, Animal)) and sprite.visible:  
                        obj_center = pygame.math.Vector2(sprite.rect.center)
                        distancia = player_center.distance_to(obj_center)
                        if distancia < 110 and (isinstance(sprite, NPC)):
                            sprite.talk(self.dialogue, self.inventory, sprite.personaje)
                            self.personaje_actual = sprite.personaje
                            self.set_talk_with(self.personaje_actual)
                        elif distancia < 110 and (isinstance(sprite, Animal)):
                            sprite.talk_animal(self.dialogue,self.draw, self.inventory, sprite.personaje)
                            self.personaje_actual = sprite.personaje
                            self.set_talk_with(self.personaje_actual)
                        elif distancia < 60:  
                            if isinstance(sprite, InteractableObject):
                                sprite.interact(self.inventory, self.director, self)
                            
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

    def move(self, dt):
        # Verificar si hay movimiento
        if self.direction.magnitude() != 0:
            # Normalizar el vector de dirección
            self.direction.normalize_ip()
            # Calcular la nueva posición con la velocidad y el tiempo transcurrido
            new_pos = self.pos + self.direction * self.speed * dt
            new_rect = self.rect.copy()
            new_rect.center = new_pos
            if not self.dialogue.obtener_dialogo():
                # Verificar colisiones antes de actualizar la posición
                if not self.check_collision(new_rect):
                    self.pos = new_pos
                    self.rect.center = self.pos

    def set_position(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.rect.topleft = self.pos

    def set_collision_layer(self, collision_layer):
        self.collision_layer = collision_layer

    # Verifica las colisiones y los cambios de escenario.
    def check_collision(self, new_rect):
        for obj in self.collision_layer:
            col_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if new_rect.colliderect(col_rect):
                if obj.name == "puertawuan":
                    self.level.change_map("./code/mapa/casas/casawuan.tmx", False, "wuan")
                    return True
                if obj.name == "salidawuan":
                    self.level.change_map(self.level.main_tmx_map, True, "exterior_wuan")
                    return True
                elif obj.name == "puertaeva":
                    self.level.change_map("./code/mapa/casas/tiendaeva.tmx", False, "eva")
                    return True
                elif obj.name == "salidaeva":
                    self.level.change_map(self.level.main_tmx_map, True, "exterior_eva")
                    return True
                elif obj.name == "puertaxoel":
                    self.level.change_map("./code/mapa/casas/tiendaxoel.tmx", False, "xoel")
                    return True
                elif obj.name == "salidaxoel":
                    self.level.change_map(self.level.main_tmx_map, True, "exterior_xoel")
                    return True
                elif obj.name == "parking":
                    self.level.change_map("./code/mapa/parking/parking.tmx", False, "parking")
                    return True
                elif obj.name == "salida_parking":
                    self.level.change_map(self.level.main_tmx_map, True, "exterior_parking")
                    return True
                elif obj.name == "playa":
                    self.level.change_map("./code/mapa/playa/playa.tmx", False, "playa")
                    return True
                elif obj.name == "salida_playa":
                    self.level.change_map(self.level.main_tmx_map, True, "exterior_playa")
                    return True
                elif obj.name == "cementerio":
                    self.level.change_map("./code/mapa/cementerio/cementerio.tmx", False, "cementerio")
                    return True
                elif obj.name == "salida_cementerio":
                    self.level.change_map(self.level.main_tmx_map, True, "exterior_cementerio")
                    return True
                elif obj.name == "puertafinal":
                    if self.level.escene == "Nivel3":
                        if self.draw.dibujar_cartel(self.inventory):
                            self.level.change_map("./code/mapa/final/final.tmx", False, "final1")
                        return True
                elif obj.name == "puertafinal2":
                    self.puzle.start_puzle()     
                    self.level.change_map("./code/mapa/final/final2.tmx", False, "final2")              
                    return True
                else:
                    return True
        # Si no se detectan colisiones, se devuelve False
        return False

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.velocity = self.direction * self.speed  # Actualizar la velocidad basada en la dirección
        self.move(dt)
        self.animate(dt)

    # Funciones que podran accederse desde Objectives
    def is_cut_down_tree(self):
        return self.cut_down_tree

    def set_talk_with(self, personaje):
        self.talk_with_list[personaje] = True

    def talk_with(self, personaje):
        if personaje in self.talk_with_list:
            return self.talk_with_list[personaje]

    def puzle_is_complete(self):
        return self.puzle.get_is_complete()

    def set_interact_with_last_object(self, opcion):
        self.interact_last_object = opcion
    
    def get_interact_with_last_object(self):
        return self.interact_last_object