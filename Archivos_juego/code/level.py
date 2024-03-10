import pygame
import pytmx
from settings import *
from sprites import *
from player import Player, InteractableObject, Dialogue
from overlay import Overlay
from inventory import Inventory
from pytmx.util_pygame import load_pygame
from npc import NPC
from draw import Draw
from tutorial import Tutorial
from animals import Animal
import time
import os
from dialogue_strategy import Dialogue_Strategy
from objectives import Objectives

class Level:
    def __init__(self, soil_layer, all_sprites, screen, escene):
        self.display_surface = pygame.display.get_surface()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.camera = pygame.math.Vector2()

        self.escene = escene
        self.screen = screen

        # Dialogue
        self.dialogue = Dialogue(self.screen)
        self.inventory = Inventory(self.screen)

        self.draw = Draw(self.screen)
        self.dialogue_strategy = Dialogue_Strategy(self.draw)

        self.soil_layer = soil_layer
        self.all_sprites = all_sprites
        self.setup()
        
        # Overlay 
        self.overlay = Overlay(self.player)
        
        # Tutorial
        self.tutorial = Tutorial(self.screen)

        # Objetives
        self.objectives = Objectives(self.screen, self.inventory, self.dialogue, self.player, self.soil_layer, self.opcion_mapa)

    def setup(self):
        
        self.zoom = 4

        maps = {"verano": "mapa_verano22", "otoño": "mapa_otoño2", "invierno": "mapa_invierno2", "volcan": "volcan"}
        
        player_start_x = 1800
        player_start_y = 4000


        if self.escene == "Nivel1":

            # Cargar el mapa de Tiled
            self.opcion_mapa = "verano"
            extension = maps.get(self.opcion_mapa, "pruebas2")
            self.main_tmx_map = "./code/mapa/verano/mapa_verano.tmx"
            self.tmx_map = load_pygame(self.main_tmx_map)

            # trees 
            for obj in self.tmx_map.get_layer_by_name('arboles'):
                Tree( pos = (obj.x *5 + obj.x/10, obj.y * 7 + obj.y/2.5), surf = obj.image, groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], name = obj.name, inventory=self.inventory)

            # Obtener la capa de colisiones
            self.collision_layer = self.tmx_map.get_layer_by_name("colisiones")

            #Crear el jugador en la posición deseada
            self.player = Player((player_start_x, player_start_y), self.all_sprites, self.collision_layer, self.soil_layer, tree_sprites=self.tree_sprites,  inventory=self.inventory, level=self, dialogue=self.dialogue)

            self.npcs = self.create_npcs()
            self.objects = self.create_objects()
            self.animals = []

        elif self.escene == "Nivel2":

            # Cargar el mapa de Tiled
            self.opcion_mapa = "otoño"   # Cambiar este string para cambiar de mapa
            extension = maps.get(self.opcion_mapa, "pruebas2")
            self.main_tmx_map = "./code/mapa/otoño/mapa_otoño.tmx"
            self.tmx_map = load_pygame(self.main_tmx_map)

            # trees 
            for obj in self.tmx_map.get_layer_by_name('arboles'):
                Tree( pos = (obj.x *5 + obj.x/10, obj.y * 7 + obj.y/2.5), surf = obj.image, groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], name = obj.name, inventory=self.inventory)

            # Obtener la capa de colisiones
            self.collision_layer = self.tmx_map.get_layer_by_name("colisiones")

            self.player = Player((player_start_x, player_start_y), self.all_sprites, self.collision_layer, self.soil_layer, tree_sprites=self.tree_sprites,  inventory=self.inventory, level=self, dialogue=self.dialogue)

            self.npcs = self.create_npcs()
            self.objects = self.create_objects()
            self.animals = self.create_animals()

        elif self.escene == "Nivel3":
            # Cargar el mapa de Tiled
            self.opcion_mapa = "invierno"   # Cambiar este string para cambiar de mapa
            extension = maps.get(self.opcion_mapa, "pruebas2")
            self.main_tmx_map = "./code/mapa/invierno/mapa_invierno.tmx"
            self.tmx_map = load_pygame(self.main_tmx_map)

            # trees 
            for obj in self.tmx_map.get_layer_by_name('arboles'):
                Tree( pos = (obj.x *5 + obj.x/10, obj.y * 7 + obj.y/2.5), surf = obj.image, groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], name = obj.name, inventory=self.inventory)

            # Obtener la capa de colisiones
            self.collision_layer = self.tmx_map.get_layer_by_name("colisiones")

            self.player = Player((player_start_x, player_start_y), self.all_sprites, self.collision_layer, self.soil_layer, tree_sprites=self.tree_sprites,  inventory=self.inventory, level=self, dialogue=self.dialogue)

            self.npcs = self.create_npcs()
            self.objects = self.create_objects()
            self.animals = self.create_animals()

        # Ajustar la posición y el tamaño de los objetos en el mapa
        for obj in self.collision_layer:
            obj.x *= self.zoom  # Aumentar la posición x
            obj.y *= self.zoom  # Aumentar la posición y
            obj.width *= self.zoom  # Aumentar el ancho
            obj.height *= self.zoom  # Aumentar la altura


    def show_loading_screen(self):
        # Directorio donde se encuentran las imágenes del GIF
        gif_folder = './code/sprites/pantalla_carga/gif_cargando'

        # Obtener la lista de archivos en el directorio
        gif_files = sorted(os.listdir(gif_folder))

        # Cargar y mostrar cada imagen en la carpeta
        for file_name in gif_files:
            file_path = os.path.join(gif_folder, file_name)
            image = pygame.image.load(file_path).convert_alpha()

            # Escalar la imagen para que encaje en la pantalla
            original_width, original_height = image.get_size()
            new_height = SCREEN_HEIGHT
            new_width = int((new_height / original_height) * original_width)
            image = pygame.transform.scale(image, (new_width, new_height))

            # Mostrar la imagen en la pantalla de carga
            self.display_surface.blit(image, (0, 0))
            pygame.display.flip()
        
    def change_map(self, path, outside, place):
            
        if not outside:
            for tree in self.tree_sprites.sprites():
                tree.make_invisible()
        else:
            for tree in self.tree_sprites.sprites():
                    tree.make_visible()
    
        #Crear el jugador en la posición deseada
        if(place == "exterior_wuan"):
            for npc in self.npcs:
                npc.make_invisible("fuera")

            for animal in self.animals:
                animal.make_invisible("fuera")

            for object in self.objects:
                object.make_invisible("fuera")

            self.player.set_position(1800, 3850)
        elif(place == "wuan"):
            for npc in self.npcs:
                npc.make_invisible("wuan")
                
            for animal in self.animals:
                animal.make_invisible("wuan")

            for object in self.objects:
                object.make_invisible("wuan")
            
            self.player.set_position(1150, 1290)
        elif(place == "exterior_eva"):
            for npc in self.npcs:
                npc.make_invisible("fuera")

            for animal in self.animals:
                animal.make_invisible("fuera")

            for object in self.objects:
                object.make_invisible("fuera")
            
            self.player.set_position(1810, 1470)
        elif(place == "eva"):
            for npc in self.npcs:
                npc.make_invisible("eva")

            for animal in self.animals:
                animal.make_invisible("eva")

            for object in self.objects:
                object.make_invisible("eva")
                
            self.player.set_position(1280, 1100)
        elif(place == "xoel"):      
            for npc in self.npcs:
                npc.make_invisible("xoel")

            for animal in self.animals:
                animal.make_invisible("xoel")

            for object in self.objects:
                object.make_invisible("xoel")

            self.player.set_position(1090, 1280)
                
        elif(place == "exterior_xoel"):
            for npc in self.npcs:
                npc.make_invisible("fuera")

            for animal in self.animals:
                animal.make_invisible("fuera")

            for object in self.objects:
                object.make_invisible("fuera")
                    
            self.player.set_position(2180, 1470)
        if(place == "exterior_playa"):
            for npc in self.npcs:
                npc.make_invisible("fuera")

            for animal in self.animals:
                animal.make_invisible("fuera")

            for object in self.objects:
                object.make_invisible("fuera")

            self.player.set_position(3100, 4430)
        elif(place == "playa"):
            for npc in self.npcs:
                npc.make_invisible("playa")
                
            for animal in self.animals:
                animal.make_invisible("playa")

            for object in self.objects:
                object.make_invisible("playa")

            self.player.set_position(1100, 1480)
        if(place == "exterior_cementerio"):
            for npc in self.npcs:
                npc.make_invisible("fuera")

            for animal in self.animals:
                animal.make_invisible("fuera")

            for object in self.objects:
                object.make_invisible("fuera")

            self.player.set_position(3100, 2570)
        elif(place == "cementerio"):
            for npc in self.npcs:
                npc.make_invisible("cementerio")
                
            for animal in self.animals:
                animal.make_invisible("cementerio")

            for object in self.objects:
                object.make_invisible("cementerio")

            self.player.set_position(1800, 3850)
        if(place == "exterior_parking"):
            for npc in self.npcs:
                npc.make_invisible("fuera")

            for animal in self.animals:
                animal.make_invisible("fuera")

            for object in self.objects:
                object.make_invisible("fuera")

            self.player.set_position(710, 2570)
        elif(place == "parking"):
            for npc in self.npcs:
                npc.make_invisible("parking")
                
            for animal in self.animals:
                animal.make_invisible("parking")

            for object in self.objects:
                object.make_invisible("parking")

            self.player.set_position(2400, 1470)
        elif(place == "final1"):
            for npc in self.npcs:
                npc.make_invisible("final1")

            for animal in self.animals:
                animal.make_invisible("final1")

            for object in self.objects:
                object.make_invisible("final1")

            self.player.set_position(1180, 1000)
        elif(place == "final2"):
            for npc in self.npcs:
                npc.make_invisible("final2")

            for animal in self.animals:
                    animal.make_invisible("final2")

            for object in self.objects:
                 object.make_invisible("final2")

            self.player.set_position(990, 1170)
        
        # Mostrar pantalla de carga
        self.show_loading_screen()

        #Cargar el mapa de Tiled
        self.tmx_map = load_pygame(path)
        # Obtener la capa de colisiones
        self.collision_layer = self.tmx_map.get_layer_by_name("colisiones")
        self.player.set_collision_layer(self.collision_layer)
    
    
        # Ajustar la posición y el tamaño de los objetos en el mapa
        for obj in self.collision_layer:
            obj.x *= self.zoom  # Aumentar la posición x
            obj.y *= self.zoom  # Aumentar la posición y
            obj.width *= self.zoom  # Aumentar el ancho
            obj.height *= self.zoom  # Aumentar la altura
    


    def create_objects(self):
        objects_list = []


        objects_list.append(InteractableObject(
            pos=(1600, 4100),
            group=self.all_sprites, color=(255, 128, 0), dialogue=self.dialogue, sprite="./code/sprites/icono.png", interactable_type="Fin", location="fuera"))

        if self.escene == "Nivel1":

            objects_list.append(InteractableObject(
                pos=(1800, 4100),
                group=self.all_sprites, color=(255, 128, 0), dialogue=self.dialogue, sprite="./code/sprites/madera.png", interactable_type="madera", location="fuera"))
            
            objects_list.append(InteractableObject(
                pos=(1800, 4300),
                group=self.all_sprites, color=(255, 128, 0), dialogue=self.dialogue, sprite="./code/sprites/madera.png", interactable_type="madera", location="fuera"))
            
            objects_list.append(InteractableObject(
                pos=(1800, 4500),
                group=self.all_sprites, color=(255, 128, 0), dialogue=self.dialogue, sprite="./code/sprites/madera.png", interactable_type="madera", location="fuera"))
            
            objects_list.append(InteractableObject(
                pos=(1700, 4000),
                group=self.all_sprites,color=(0,0,255),dialogue=self.dialogue, sprite="./code/sprites/dinero.png", interactable_type="dinero", location="fuera"))      

        else:
            objects_list.append(InteractableObject(
                pos=(1700, 4100),
                group=self.all_sprites, color=(255, 255, 0),dialogue=self.dialogue, sprite="./code/sprites/trigo.png", interactable_type="trigo", location="fuera"))
        
        return objects_list

    def create_npcs(self):
        npcs_list = []
        
        if self.escene == "Nivel1":
            npcs_list.append(NPC(
                pos=(SCREEN_WIDTH / 2 + 550 , SCREEN_HEIGHT / 2 + 570),
                group=self.all_sprites, sprite_directory="./code/sprites/NPC/Don_Diego_el_VIEJO",inventory=self.inventory, dialogue=self.dialogue,personaje="don diego", location="wuan"))
            
            npcs_list.append(NPC(
                pos=(2000, 3850),
                group=self.all_sprites, sprite_directory="./code/sprites/NPC/Jordi_el_obrero",inventory=self.inventory, dialogue=self.dialogue,personaje="butanero", location="fuera"))
            
            npcs_list.append(NPC(
                pos=(2000, 4000),
                group=self.all_sprites, sprite_directory="./code/sprites/NPC/Xoel_el_tendero",inventory=self.inventory, dialogue=self.dialogue,personaje="mercader", location="fuera"))
            
        else:
            npcs_list.append(NPC(
                pos=(860, 836),
                group=self.all_sprites, sprite_directory="./code/sprites/NPC/Don_Diego_el_VIEJO",inventory=self.inventory, dialogue=self.dialogue,personaje="don diego", location="wuan"))

            npcs_list.append(NPC(
                pos=(SCREEN_WIDTH / 2 + 680 , SCREEN_HEIGHT / 2 + 505),
                group=self.all_sprites, sprite_directory="./code/sprites/NPC/Eva_la_modista",inventory=self.inventory, dialogue=self.dialogue,personaje="modista", location="eva"))
            
            npcs_list.append(NPC(
                pos=(SCREEN_WIDTH / 2 + 550 , SCREEN_HEIGHT / 2 + 570),
                group=self.all_sprites, sprite_directory="./code/sprites/NPC/Xoel_el_tendero",inventory=self.inventory, dialogue=self.dialogue,personaje="mercader", location="xoel"))
            
            npcs_list.append(NPC(
                pos=(2360, 2540),
                group=self.all_sprites, sprite_directory="./code/sprites/NPC/Pablo_y_Manu",inventory=self.inventory, dialogue=self.dialogue,personaje="hermanos", location="fuera"))
            
        return npcs_list

    def create_animals(self):
        animals_list = []
        if self.escene == "Nivel2":
            # Posicion animales
            pass
        else:
            # Posicion animales
            pass
        
        animals_list.append(Animal(
            pos=(SCREEN_WIDTH / 2 + 300  , SCREEN_HEIGHT / 2 + 2500), group=self.all_sprites, animal_type="oveja", inventory=self.inventory, dialogue=self.dialogue,personaje="oveja", prime=True, walk=3, location="playa"))
        
        
        animals_list.append(Animal(
            pos=(SCREEN_WIDTH / 2 + 500 , SCREEN_HEIGHT / 2 + 2000),
            group=self.all_sprites, animal_type="pollo", inventory=self.inventory, dialogue=self.dialogue,personaje="pollo", walk=1, location="cementerio"))
        
        
        animals_list.append(Animal(
            pos=(SCREEN_WIDTH / 2 + 500 , SCREEN_HEIGHT / 2 + 1200),
            group=self.all_sprites, animal_type="vaca_marron", inventory=self.inventory, dialogue=self.dialogue,personaje="vaca", prime=True, walk=2, location="parking"))
        
        
        return animals_list
        

    def run(self, dt, key_z_pressed, left_mouse_button_down, event_mouse, tutorial_enabled):
        self.display_surface.fill('black')

        # Centrar la cámara en el jugador
        self.camera.x = self.player.rect.centerx - SCREEN_WIDTH / 2
        self.camera.y = self.player.rect.centery - SCREEN_HEIGHT / 2

        # Dibujar el fondo desde el mapa de Tiled
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        # Ajustar el tamaño de la imagen del fondo
                        scaled_tile = pygame.transform.scale(tile, (int(tile.get_width() * self.zoom), int(tile.get_height() * self.zoom)))
                        self.display_surface.blit(scaled_tile, (x * self.tmx_map.tilewidth * self.zoom - self.camera.x,
                                                                y * self.tmx_map.tileheight * self.zoom - self.camera.y))

        self.all_sprites.custom_draw(self.player, self.zoom, self.tree_sprites)
        self.all_sprites.update(dt)
        self.plant_collision()

        # Mover al jugador
        self.player.move(dt)

        # Para mostrar el overlay
        self.overlay.display()
        
        # Tutorial
        self.tutorial.mostrar_tutorial(key_z_pressed, tutorial_enabled)
        
        self.objectives.evaluate()

        # Dropdown
        self.objectives.show_dropdown(left_mouse_button_down, event_mouse)

        
    def check_collision(self):
        player_rect = self.player.rect

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.rect):
                    # Añadir una unidad de trigo al inventario
                    self.player.inventory.añadir_trigo()
                    plant.kill()

                    # Coordenadas del tile
                    x = plant.rect.centerx // TILE_SIZE
                    y = plant.rect.centery // TILE_SIZE
                    if 'S' in self.soil_layer.grid[y][x]:
                        self.soil_layer.grid[y][x].remove('S')
                    if 'W' in self.soil_layer.grid[y][x]:
                        self.soil_layer.grid[y][x].remove('W')
                        # Eliminar el agua del tile
                        for water_sprite in self.soil_layer.water_sprites.sprites():
                            if water_sprite.rect.collidepoint((x * TILE_SIZE, y * TILE_SIZE)):
                                water_sprite.kill()

    def clean_level(self):
        # Eliminar todos los sprites del grupo de sprites y reiniciar listas de objetos
        self.all_sprites.empty()
        self.tree_sprites.empty()
        self.collision_sprites.empty()
        self.npcs.clear()
        self.objects.clear()
        self.animals.clear()
                
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.camera = pygame.math.Vector2()

    def custom_draw(self, player, zoom, tree_sprites):
        # Cámara sigue al jugador
        self.camera.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.camera.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == 7:
                    scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width) * zoom, int(sprite.rect.height) * zoom))
                elif sprite.z == 6:
                    scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width) / zoom, int(sprite.rect.height) / zoom))
                else:
                    scaled_image = pygame.transform.scale(sprite.image, (int(sprite.rect.width), int(sprite.rect.height)))
                    
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    
                    if sprite in tree_sprites:
                        # Ajustar la posición del árbol para dibujar correctamente
                        offset_rect.centery -= sprite.rect.height * 0.9
                        scaled_rect = scaled_image.get_rect(center=(offset_rect.centerx - self.camera.x, offset_rect.centery - self.camera.y))
                    else:
                        offset_rect.center -= self.camera
                        scaled_rect = scaled_image.get_rect(center=offset_rect.center)
                    self.display_surface.blit(scaled_image, scaled_rect.topleft)
