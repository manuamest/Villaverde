import pygame
import sys
from director import Director

if __name__ == '__main__':
    # Inicializamos pygame
    pygame.init()

    # Creamos al director
    director = Director()

    # Ejecutamos el juego
    director.run()

    # Cuando termine la ejecucion finaliza la libreria
    pygame.quit()
