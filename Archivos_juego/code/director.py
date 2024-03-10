import pygame
import sys
import time
from soil import SoilLayer
from level import Level, CameraGroup
from settings import *
from menu import Menu
from moviepy.editor import VideoFileClip
import os

class Director:
    def __init__(self):
        
        # Inicializamos la pantalla, con un icono y el modo grafico
        #self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        icon_path = "./code/sprites/icono.png"
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Villaverde')

        # Pila de escenas
        self.pila = []

        # Flag para salir de la escena
        self.salir_escena = False

        # Reloj
        self.clock = pygame.time.Clock()

        # Ajustes necesarios en el futuro para los levels
        self.all_sprites = CameraGroup()
        self.soil_layer = SoilLayer(self.all_sprites)
        self.last_growth_time = time.time()
        self.level = Level(self.soil_layer, self.all_sprites, self.screen, "Nivel1")
        self.menu = Menu(self.screen, self.clock)

        # Obtener la ruta actual del archivo
        current_path = os.path.dirname(os.path.abspath(__file__))
        
        # Ruta del archivo de video (relativa al directorio actual)
        video_filename = 'videos/intro.mp4'
        
        # Concatenar la ruta actual con la ruta del archivo de video
        self.video_path = os.path.join(current_path, video_filename)
        self.video_clip = VideoFileClip(self.video_path)
        self.video_duration = self.video_clip.duration

        self.paused = False
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay_surface.set_alpha(10)  # Configura la transicion


    def run(self):
        escena1 = 1
        #self.bucle(escena=escena1)
        self.menu.show_start_screen()
        self.menu.run()
        self.tutorial_enabled = self.menu.tutorial_enabled
        self.bucle(escena=escena1)
        self.level.clean_level()
        self.tutorial_enabled = False
        # Crea un nuevo nivel y repite el bucle
        self.level = Level(self.soil_layer, self.all_sprites, self.menu.screen, "Nivel2")
        self.bucle(escena=escena1)
        self.level.clean_level()

        # Repite el proceso para los demás niveles
        self.level = Level(self.soil_layer, self.all_sprites, self.screen, "Nivel3")
        self.bucle(escena=escena1)
        self.level.clean_level()
            
        #self.play_video_intro()

    def _update_plants(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_growth_time

        if elapsed_time >= 5:
            self.soil_layer.update_plants() 
            self.last_growth_time = current_time

    def bucle(self, escena):
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

            if not self.paused:  # Solo actualizar si no está en pausa
                self._update_plants()
                dt = self.clock.tick(FPS) / 700
                self.level.run(dt, self.key_z_pressed, left_mouse_button_down, event_mouse, self.tutorial_enabled)
                pygame.display.update()
            else:
                self.screen.blit(self.overlay_surface, (0, 0))  # Agrega el filtro oscuro

                # Muestra las opciones de continuar y salir del juego
                self.menu.show_pause_menu()

                pygame.display.update()
            
            self.salir_escena = self.level.inventory.salir_escena


    def play_video_intro(self):
        # Reproducir el video de introducción
        self.video_clip.preview()

    def ejecutar(self):

        # Mientras haya escenas en la pila, ejecutaremos la de arriba
        while(len(self.pila) > 0):
            # Se toma la escena de la cima
            escena = self.pila[len(self.pila) -1 ]

            # Ejecutamos el bucle hasta que termine la escena
            self.bucle(escena)

    def salirEscena(self):
    
        # Indicamos en el flag que se quiere salir de la escena
        self.salir_escena = True
    
        # Eliminamos la escena actual de la pila (si la hay)
        if (len(self.pila)>0):
            self.pila.pop()
    
    def salirPrograma(self):
    
        # Vaciamos la lista de escenas pendientes
        self.pila = []
        self.salir_escena = True
    
    def cambiarEscena(self, escena):
        self.salirEscena()
    
        # Ponemos la escena pasada en la cima de la pila
        self.pila.append(escena)
    
    def apilarEscena(self, escena):
        self.salir_escena = True
    
        # Ponemos la escena pasada en la cima de la pila
        self.pila.append(escena)


if __name__ == '__main__':
    director = Director()
    director.run()
