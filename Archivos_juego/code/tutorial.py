import pygame
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from timer import Timer

class Tutorial:
    def __init__(self):
        self.pantalla_ancho, self.pantalla_alto = SCREEN_WIDTH, SCREEN_HEIGHT
        self.pantalla = pygame.display.set_mode((self.pantalla_ancho, self.pantalla_alto))

        
        self.imagen_fondo_tutorial = pygame.image.load('./code/sprites/tutorial/tutorial.png').convert_alpha()
        self.imagen_fondo_tutorial.set_alpha(150)
        
        self.indice_tutorial = 0
        self.tutorial_mensajes = [
            "¡Bienvenido a Villaverde! Usa las teclas A,W,S,D para mover al jugador. Dale a la 'Z' para seguir.",
            "Ahora para cambiar de herramienta presiona la tecla 'Q' y para usarla dale al 'SPACE'.",
            "Para recoger objetos, simplemente camina sobre ellos y presiona la tecla 'E'.",
            "¡Muy bien! Ahora, vamos a ver tu inventario. Presiona la tecla 'B' para abrirlo.",
            "En el inventario, puedes ver los objetos que has recogido. ¡Ciérralo presionando 'B' de nuevo!",
            "Vamos a hablar con el NPC. Acércate a él y presiona la tecla 'E'." ,
            "Usa la tecla 'X' para avanzar en el diálogo o seleccionar una opcion. Si necesitas escoger una opcion presiona 'UP' o 'DOWN'.",
            "¡Felicidades! Has completado el tutorial. ¡Disfruta del juego!"
        ]
        self.tutorial_on = False
        self.tutorial_surface = pygame.Surface((800, 100))
        self.tutorial_rect = self.tutorial_surface.get_rect(center=(400, 550))
        
        # Letra
        self.MARRON = (128, 58, 58)
        self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)
        self.longitud_actual = 0
        
        self.velocidad_texto = 0.05
        self.update = time.time()
        self.tiempo_espera = 1.5  # segundos de espera antes de cambiar al siguiente mensaje
        self.timers = {'tutorial': Timer(1000)}
        

    def activar_tutorial(self):
        self.tutorial_on = True
        self.indice_tutorial = 0
        
    def desactivar_tutorial(self):
        self.tutorial_on = False
        self.indice_tutorial = 0
    
    def reiniciar_letras(self):
        self.longitud_actual = 0
        self.update = time.time()
    
    def mostrar_tutorial(self):
        if self.tutorial_on:
            tiempo_actual = time.time()
            
            texto = self.tutorial_mensajes[self.indice_tutorial]
            dialogo_ancho, dialogo_alto = 850, 180
            dialogo_x = self.pantalla_ancho - dialogo_ancho
            dialogo_y = (self.pantalla_alto // 2 - dialogo_alto // 2) - dialogo_alto
            inicio_texto_x ,inicio_texto_y = dialogo_x + 30, dialogo_y + 30
            
            self.pantalla.blit(self.imagen_fondo_tutorial, (dialogo_x, dialogo_y))

            if tiempo_actual - self.update > self.velocidad_texto:
                if self.longitud_actual < len(texto):
                    self.longitud_actual += 1
                    self.ultimo_update = tiempo_actual

            texto_mostrado = texto[:self.longitud_actual]
            self.mostrar_texto(texto_mostrado, inicio_texto_x, inicio_texto_y)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        print(f'INDICE:{self.indice_tutorial}')
                        self.indice_tutorial += 1
                        if self.indice_tutorial >= len(self.tutorial_mensajes):
                            self.desactivar_tutorial()
                        else:
                            self.reiniciar_letras()
        

    def mostrar_texto(self, texto_mostrado, inicio_texto_x, inicio_texto_y):
        max_ancho_linea = 350
        palabras = texto_mostrado.split(' ')
        linea_actual = ""
        y_offset = 0
        
        for palabra in palabras:
            prueba_linea = f"{linea_actual} {palabra}" if linea_actual else palabra
            prueba_superficie = self.fuente.render(prueba_linea, True, self.MARRON)
            prueba_ancho = prueba_superficie.get_width()

            if prueba_ancho <= max_ancho_linea:
                linea_actual = prueba_linea
            else:
                self.pantalla.blit(self.fuente.render(linea_actual, True, self.MARRON),
                                   (inicio_texto_x, inicio_texto_y + y_offset))
                y_offset += 30
                linea_actual = palabra
                
        if linea_actual:
            self.pantalla.blit(self.fuente.render(linea_actual, True, self.MARRON),(inicio_texto_x, inicio_texto_y + y_offset))

