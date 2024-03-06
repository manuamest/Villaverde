import pygame
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from timer import Timer
from objectives import Objectives


class Tutorial:
    def __init__(self, screen, objective_index):
        self.pantalla = screen
        self.imagen_fondo_tutorial = pygame.image.load('./code/sprites/tutorial/tutorial.png').convert_alpha()
        self.posicion = self.imagen_fondo_tutorial.get_rect().topleft
        self.margen = 35

        self.indice_tutorial = 0 if objective_index == None else objective_index
        self.tutorial_mensajes = [
            "Bienvenido a Villaverde! Usa las teclas A,W,S,D para mover al jugador. Dale a la 'Z' para seguir.",
            "Ahora para cambiar de herramienta presiona la tecla 'Q' y para usarla dale al 'SPACE'.",
            "Para recoger objetos, simplemente camina sobre ellos y presiona la tecla 'E'.",
            "Muy bien! Ahora, vamos a ver tu inventario. Presiona la tecla 'B' para abrirlo. Cierralo presionando 'B' de nuevo!",
            "Vamos a hablar con el NPC. Acercate a el y presiona la tecla 'E'.",
            "Usa la tecla 'X' para avanzar en el dialogo o seleccionar una opcion. Si necesitas escoger una opcion presiona 'UP' o 'DOWN'.",
            "Clica en la esquina superior derecha para ver los objetivos y vuelve a clicar para cerrar el desplegable",
            "Felicidades! Has completado el tutorial. Disfruta del juego!"
        ]
        if objective_index == None or objective_index < len(self.tutorial_mensajes):
            self.tutorial_on = True
        else:
            self.tutorial_on = False

        # Letra
        self.MARRON = (59, 31, 10)
        self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)
        self.longitud_actual = 0

        self.velocidad_texto = 0.05
        self.update = time.time()

        # Continuar tutorial
        self.next_step = False

    def activar_tutorial(self):
        self.tutorial_on = True
        self.indice_tutorial = 0

    def desactivar_tutorial(self):
        self.tutorial_on = False
        self.indice_tutorial = 0

    def is_tutorial_on(self):
        return self.tutorial_on

    def reiniciar_letras(self):
        self.longitud_actual = 0
        self.update = time.time()

    def mostrar_tutorial(self, key_z_pressed):
        if self.tutorial_on:
            tiempo_actual = time.time()
            texto = self.tutorial_mensajes[self.indice_tutorial]

            self.pantalla.blit(self.imagen_fondo_tutorial, self.posicion)

            if tiempo_actual - self.update > self.velocidad_texto:
                if self.longitud_actual < len(texto):
                    self.longitud_actual += 1
                    self.ultimo_update = tiempo_actual

            texto_mostrado = texto[:self.longitud_actual]
            self.mostrar_texto(texto_mostrado, self.posicion)
            if self.next_step and key_z_pressed:
                self.indice_tutorial += 1
                self.next_step = False
                if self.indice_tutorial >= len(self.tutorial_mensajes):
                    self.desactivar_tutorial()
                else:
                    self.reiniciar_letras()

    def mostrar_texto(self, texto_mostrado, posicion):
        max_ancho_linea = 350
        palabras = texto_mostrado.split(' ')
        linea_actual = ""
        espacio_entre_lineas = 0
        inicio_texto_x, inicio_texto_y = (
            elemento + self.margen for elemento in posicion)

        for palabra in palabras:
            prueba_linea = f"{linea_actual} {palabra}" if linea_actual else palabra
            prueba_superficie = self.fuente.render(prueba_linea, True, self.MARRON)
            prueba_ancho = prueba_superficie.get_width()

            if prueba_ancho <= max_ancho_linea:
                linea_actual = prueba_linea
            else:
                self.pantalla.blit(self.fuente.render(linea_actual, True, self.MARRON),
                                   (inicio_texto_x, inicio_texto_y + espacio_entre_lineas))
                espacio_entre_lineas += 30
                linea_actual = palabra

        if linea_actual:
            self.pantalla.blit(self.fuente.render(linea_actual, True, self.MARRON),
                               (inicio_texto_x, inicio_texto_y + espacio_entre_lineas))

    def enable_next_step(self):
        self.next_step = True
