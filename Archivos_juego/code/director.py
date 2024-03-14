import pygame
import sys
import time
from soil import SoilLayer
from level import Level, CameraGroup
from settings import *
from menu import Menu
from inventory import Inventory
from moviepy.editor import VideoFileClip
import os
from pyvidplayer import Video

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
        self.levels = [Level(self.soil_layer, self.all_sprites, self.screen,self.inventory, "Nivel1"),
                        Level(self.soil_layer, self.all_sprites, self.screen,self.inventory, "Nivel2"),
                        Level(self.soil_layer, self.all_sprites, self.screen,self.inventory, "Nivel3")]
        self.menu = Menu(self.screen, self.clock)

        self.paused = False
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay_surface.set_alpha(10)  # Configura la transicion

        # Cinematica y creditos
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.intro_name = 'videos/intro.mp4'
        self.credits_name = 'videos/creditos.mp4'

    def run(self):

        self.menu.show_start_screen()
        self.menu.run()
        self.tutorial_enabled = self.menu.tutorial_enabled
        
        #self.playIntro()

        for level in self.levels:
            level.setup()
            self.show_level_text = True
            self.level_start_time = time.time()
            self.bucle(level)
            level.clean_level()
            self.tutorial_enabled = False
        
        self.playCredits()
                
    def playIntro(self):
        self.video_path = os.path.join(self.current_path, self.intro_name)
        self.intro = Video(self.video_path)
        self.intro.set_size((SCREEN_WIDTH, SCREEN_HEIGHT))
        while self.intro.active:
            self.intro.draw(self.screen, (0,0))
            pygame.display.update()

    def playCredits(self):
        self.video_path = os.path.join(self.current_path, self.credits_name)
        self.credits = Video(self.video_path)
        self.credits.set_size((SCREEN_WIDTH, SCREEN_HEIGHT))
        while self.credits.active:
            self.credits.draw(self.screen, (0,0), force_draw=False)
            pygame.display.update()

    def _update_plants(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_growth_time

        if elapsed_time >= 5:
            self.soil_layer.update_plants() 
            self.last_growth_time = current_time

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
            else:
                self.screen.blit(self.overlay_surface, (0, 0))  # Agrega el filtro oscuro

                # Muestra las opciones de continuar y salir del juego
                self.menu.show_pause_menu()

                pygame.display.update()
            
            self.salir_escena = level.salir_escena

if __name__ == '__main__':
    director = Director()
    director.run()
