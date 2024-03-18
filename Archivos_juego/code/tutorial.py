import pygame
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from timer import Timer
from objectives import Objectives


class Tutorial:
    def __init__(self, screen, nivel):
        self.pantalla = screen
        self.imagen_fondo_tutorial = pygame.image.load('./code/sprites/tutorial/tutorial.png').convert_alpha()
        self.posicion = self.imagen_fondo_tutorial.get_rect().topleft
        self.margen = 35
        self.indice_tutorial = 0

        tutorial_verano = [
            "Bienvenido a Villaverde! Si es tu primera vez jugando, te recomendamos seguir este breve tutorial.",
            "Usa las teclas A,W,S,D para mover al jugador.",
            "Haz clic en la esquina superior derecha para ver los objetivos y vuelve a hacer clic para cerrar el desplegable.",
            "Para cambiar de herramienta, presiona la tecla 'Q' y para usarla presiona 'SPACE'.",
            "Intenta talar un arbol. Acercate con el hacha y usala. Algunos son mas duros que otros, prueba desde distintos angulos.",
            "Para recoger objetos, simplemente camina sobre ellos y/o presiona la tecla 'E'.",
            "Ahora, vamos a ver tu inventario. Presiona la tecla 'TAB' para abrirlo. Cierralo presionando 'TAB' de nuevo.",
            "Hablemos con Don Diego o Jordi el obrero. Acercate a el y presiona la tecla 'E'.",
            "Usa la tecla 'X' para avanzar en el dialogo o seleccionar una opcion. Si necesitas escoger una opcion, presiona 'UP' o 'DOWN'.",
            "Recuerda que si olvidas las teclas, puedes presionar la tecla 'Esc' para recordarlas.",
            "Felicidades! Has completado el tutorial. Disfruta del juego!"
            ]

        tutorial_otoño = [
            "Felicitaciones por llegar al nivel2! Estas progresando en tu aventura.",
            "Dirigete a una zona vallada abierta de madera, que sera terreno cultivable.",
            "Asegurate de tener la herramienta adecuada para arar y presiona 'SPACE'.",
            "Intenta plantar una semilla de trigo presionando la tecla 'F' sobre el terreno arado.",
            "Ahora, vamos a regarla con agua. Espera unos segundos. Ya tenemos nuestro trigo!",
            "Busca las tiendas!. Acercate a Xoel el mercader o a Eva la modista y presiona la tecla 'E'.",
            "Para escoger la cantidad a vender o comprar, muevete con las teclas 'LEFT' y 'RIGHT'. Para seleccionar la opcion, presiona 'X'.",
            "Sigue explorando. Recuerda que aun quedan secretos por descubrir, como encontrar a los animales perdidos."
            ]

        self.nivel = nivel
        if self.nivel == "Nivel1":
            self.tutorial_mensajes = tutorial_verano
        elif self.nivel == "Nivel2":
            self.tutorial_mensajes = tutorial_otoño
        
        self.tutorial_on = True

        # Letra
        self.MARRON = (59, 31, 10)
        self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)
        self.longitud_actual = 0

        self.velocidad_texto = 0.07
        self.update = time.time()

    def desactivar_tutorial(self):
        self.tutorial_on = False
        self.indice_tutorial = 0
    
    def get_tutorial_on(self):
        return self.tutorial_on

    def reiniciar_letras(self):
        self.longitud_actual = 0
        self.update = time.time()

    def mostrar_tutorial(self, key_z_pressed, tutorial_enabled):
        self.key_z_pressed = key_z_pressed
        if self.tutorial_on and tutorial_enabled:
            tiempo_actual = time.time()
            texto = self.tutorial_mensajes[self.indice_tutorial]
            self.pantalla.blit(self.imagen_fondo_tutorial, self.posicion)
            if tiempo_actual - self.update > self.velocidad_texto:
                if self.longitud_actual < len(texto):
                    self.longitud_actual += 1
                    self.ultimo_update = tiempo_actual
            texto_mostrado = texto[:self.longitud_actual]
            self.mostrar_texto(texto_mostrado, self.posicion)
            if self.key_z_pressed:
                self.indice_tutorial += 1
                if self.indice_tutorial >= len(self.tutorial_mensajes):
                    self.desactivar_tutorial()
                else:
                    self.reiniciar_letras()

    # Muestra el texto letra a letra
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
