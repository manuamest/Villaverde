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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        self.level = Level(self.soil_layer, self.all_sprites, self.screen, "Nivel3")
        self.menu = Menu(self.screen, self.clock, self.level, self.soil_layer, self.last_growth_time)

        # Obtener la ruta actual del archivo
        current_path = os.path.dirname(os.path.abspath(__file__))
        
        # Ruta del archivo de video (relativa al directorio actual)
        video_filename = 'videos/intro.mp4'
        
        # Concatenar la ruta actual con la ruta del archivo de video
        self.video_path = os.path.join(current_path, video_filename)
        self.video_clip = VideoFileClip(self.video_path)
        self.video_duration = self.video_clip.duration

    def run(self):
        escena1 = 1
        #self.bucle(escena=escena1)
        self.menu.show_start_screen()
        self.menu.run()
        
        #self.play_video_intro()

    def _update_plants(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_growth_time

        if elapsed_time >= 5:
            self.soil_layer.update_plants() 
            self.last_growth_time = current_time

    def bucle(self, escena):
        self.salir_escena = False

        # Eliminamos todos los eventos producidos antes de entrar al bucle
        pygame.event.clear()

        # El bucle del juego, las acciones que se realicen se harán en cada escena
        while not self.salir_escena:
            self.key_z_pressed = False   # Detecta la tecla z
            left_mouse_button_down = False
            event_mouse = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        self.key_z_pressed = True
                elif event.type == pygame.MOUSEBUTTONDOWN: # Clic del raton
                    if event.button == 1:  # Clic izquierdo
                        left_mouse_button_down = True
                        event_mouse = event

            self._update_plants()
            dt = self.clock.tick(FPS) / 700
            self.level.run(dt, self.key_z_pressed, left_mouse_button_down, event_mouse, True)
            pygame.display.update()


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
