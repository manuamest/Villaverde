import pygame
import sys
import time
from soil import SoilLayer
from level import Level, CameraGroup
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from menu import Menu

class Director:
    def __init__(self):
        
        # Inicializamos la pantalla, con un icono y el modo grafico
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
        self.last_growth_time = time.time()  # Tiempo de la última fase de crecimiento
        self.level = Level(self.soil_layer, self.all_sprites, self.screen)
        self.menu = Menu(self.screen, self.clock, self.level, self.soil_layer, self.last_growth_time)

    def run(self):
        self.menu.show_start_screen()
        self.menu.run()

    def bucle(self, escena):
        self.salir_escena = False

        # Eliminamos todos los eventos producidos antes de entrar al bucle
        pygame.event.clear()

        # El bucle del juego, las acciones que se realicen se harán en cada escena
        while not self.salir_escena:
            # Sincronizar a 60 fps
            tiempo_pasado = self.reloj.tick(60)

            # Eventos a escena
            escena.eventos(pygame.event.get())

            # Actualiza la escena
            escena.update(tiempo_pasado)

            # Se dibuja en pantalla
            escena.dibujar(self.screen)
            pygame.display.flip()

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
