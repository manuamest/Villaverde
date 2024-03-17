import pygame
import sys
import time
from soil import SoilLayer
from level import Level, CameraGroup
from settings import *
from menu import Menu
from inventory import Inventory
from pyvidplayer import Video
import os

class Director:
    def __init__(self):
        # Inicializamos la pantalla, con un icono y el modo grafico
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        icon_path = "./code/sprites/icono.png"
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Villaverde')

        # Flag para salir de la escena
        self.salir_escena = False

        # Reloj
        self.clock = pygame.time.Clock()

        # Ajustes necesarios en el futuro para los levels
        self.all_sprites = CameraGroup()
        self.soil_layer = SoilLayer(self.all_sprites)
        self.inventory = Inventory(self.screen)
        self.last_growth_time = time.time()
        self.levels = [Level(self.soil_layer, self.all_sprites, self.screen,self.inventory, "Nivel1", self),
                        Level(self.soil_layer, self.all_sprites, self.screen,self.inventory, "Nivel2", self),
                        Level(self.soil_layer, self.all_sprites, self.screen,self.inventory, "Nivel3", self)]
        self.menu = Menu(self.screen, self.clock)

        self.paused = False
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay_surface.set_alpha(10)  # Configura la transicion

        # Cinematica y creditos
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.intro_name = 'videos/intro.mp4'
        self.credits_name = 'videos/creditos.mp4'

        # Indica si esta en el penultimo objetivo
        self.nivel_precompleto = False

        # Variable para el radio del círculo de transición
        self.transition_radius = 30
        self.imagen_controles = pygame.image.load('./code/sprites/controles/controles.png').convert_alpha()
        self.imagen_controles_ampliada = pygame.transform.scale(self.imagen_controles, (800, 400))
        self.posicion_controles = (SCREEN_WIDTH//2-800//2, SCREEN_HEIGHT//2-400//2)

    def run(self):
        # Cargar música de fondo
        pygame.mixer.music.load('./code/villaverde.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Repetir infinitamente
        self.menu.show_start_screen()
        self.menu.run()
        self.transition_effect_close()  # Transición al acabar el nivel
        self.tutorial_enabled = self.menu.tutorial_enabled
        # Para detener la música de fondo
        pygame.mixer.music.stop()

        self.playVideo(self.intro_name)
        
        pygame.mixer.music.load('./code/villaverde.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Repetir infinitamente
        
        for level in self.levels:
            level.setup()
            self.transition_effect_open()  # Transición al empezar el nivel
            self.bucle(level)
            self.transition_effect_close()  # Transición al acabar el nivel
            level.clean_level()
        
        self.playVideo(self.credits_name)
                
    def playVideo(self, video_name):
        video_path = os.path.join(self.current_path, video_name)
        video = Video(video_path)
        video.set_size((SCREEN_WIDTH, SCREEN_HEIGHT))
        while video.active:
            video.draw(self.screen, (0,0))
            pygame.display.update()

    def _update_plants(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_growth_time

        if elapsed_time >= 5:
            self.soil_layer.update_plants() 
            self.last_growth_time = current_time
        
    def set_salir_escena(self, opcion):
        self.salir_escena = opcion

    def get_salir_escena(self):
        return self.salir_escena

    def set_nivel_precompleto(self, opcion):
        self.nivel_precompleto = opcion

    def get_nivel_precompleto(self):
        return self.nivel_precompleto

    def bucle(self, level):
        self.salir_escena = False
        
        while not self.salir_escena:
            self.key_z_pressed = False
            left_mouse_button_down = False
            event_mouse = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        self.key_z_pressed = True
                    elif event.key == pygame.K_ESCAPE:  # Verificar si se presionó Esc
                        self.paused = not self.paused  # Cambiar el estado de pausa
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        left_mouse_button_down = True
                        event_mouse = event

            if not self.paused:
                self._update_plants()
                dt = self.clock.tick(FPS) / 700
                level.run(dt, self.key_z_pressed, left_mouse_button_down, event_mouse, self.tutorial_enabled)
                pygame.display.update()      
                level.player.speed = 100          
            else:
                # Mostrar la imagen de los controles
                self.screen.blit(self.imagen_controles_ampliada, self.posicion_controles)
                pygame.display.flip()
                level.player.speed = 0    
        self.nivel_precompleto = False
                
    def transition_effect_open(self):
        # Animación de apertura del círculo de transición
        for i in range(30, 0, -1):  # Disminuye el radio del círculo
            pygame.draw.circle(self.screen, (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2), self.transition_radius * i)
            pygame.display.update()
            self.clock.tick(30)  # Espera 30 milisegundos entre cada cuadro del juego

    def transition_effect_close(self):
        # Animación de cierre del círculo de transición
        for i in range(1, 31):  # Aumenta el radio del círculo
            pygame.draw.circle(self.screen, (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2), self.transition_radius * i)
            pygame.display.update()
            pygame.time.delay(30)  # Pequeña pausa entre cada paso de la animación

if __name__ == '__main__':
    director = Director()
    director.run()