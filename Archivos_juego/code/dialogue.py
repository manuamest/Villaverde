import pygame
import time

from inventory import Inventory
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Dialogue:
    def __init__(self):

        self.pantalla_ancho = SCREEN_WIDTH
        self.pantalla_alto = SCREEN_HEIGHT
        self.pantalla = pygame.display.set_mode((self.pantalla_ancho, self.pantalla_alto))

        # Sonido diálogos
        pygame.mixer.init()
        self.sonido_letra = pygame.mixer.Sound("./code/sounds/beep.wav")
        self.sonido_select = pygame.mixer.Sound("./code/sounds/select.wav")

        # Letra
        self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)

        self.COLOR_LETRAS = (238, 212, 167)
        self.MARRON = (128, 58, 58)
        self.GRIS = (200, 200, 200)

        self.imagen_fondo_dialogo = pygame.image.load('./code/sprites/dialogos/dialogue_box2.png').convert_alpha()
        self.don_diego = pygame.image.load('./code/sprites/dialogos/don_diego.png').convert_alpha()
        self.butanero_jordi = pygame.image.load('./code/sprites/dialogos/jordi_butanero.png').convert_alpha()

        self.dialogos_rojo = [
            "\u200BUgh...ugh...necesito una monst...er.\u00A0", "\u200BQuerido Wuan, salva la granja...esta todo en tus manos.\u00A0",
            "\u200BEres el unico capaz de hacer que me vaya de esta vida en paz...cumple solo este favor...\u00A0"]

        self.dialogos_rosa = ["\u200BHola! Soy Jordi el butanero.\u00A0", "\u200BDame el dinero!!!\u00A0"]
        self.dialogos_rosa2 = ["\u200BWuan vamos bien, sigue asi!\u00A0"]

        self.inventory = Inventory()
        self.indice_dialogo = 0
        self.opcion_escogida = False
        self.opcion_seleccionada = 0
        self.dialogo_activo = False
        self.opcion_tiene_dinero = False
        self.dinero_dado = False
        self.longitud_actual = 0
        self.ultimo_update = time.time()
        self.velocidad_texto = 0.05

    def activar_dialogo(self):

        self.dialogo_activo = True
        self.indice_dialogo = 0

    def desactivar_dialogo(self):

        self.dialogo_activo = False

    def reiniciar_dialogo(self, personaje):

        if personaje == "don diego":
            self.longitud_actual = 0
            self.ultimo_update = time.time()

        elif personaje == "butanero":

            self.longitud_actual = 0
            self.ultimo_update = time.time()

    def avanzar_dialogo(self, personaje):
        self.indice_dialogo += 1
        if personaje == "don diego":
            if self.indice_dialogo >= len(self.dialogos_rojo):
                self.desactivar_dialogo()
                self.indice_dialogo = 0

        elif personaje == "butanero":
            if self.indice_dialogo >= len(self.dialogos_rosa):
                self.desactivar_dialogo()
                self.indice_dialogo = 0

            elif self.indice_dialogo >= len(self.dialogos_rosa2):
                self.desactivar_dialogo()
                self.indice_dialogo = 0

    def set_opcion_dinero(self, tiene_dinero):
        self.opcion_tiene_dinero = tiene_dinero

    def set_opcion_escogida(self, opcion_escogida):
        self.opcion_escogida = opcion_escogida

    def set_dinero_dado(self, dinero_dado):
        self.dinero_dado = dinero_dado

    def obtener_dinero_dado(self):
        return self.dinero_dado

    def set_opcion_seleccionada(self, opcion):
        self.opcion_seleccionada = opcion

    def obtener_opcion_seleccionada(self):
        return self.opcion_seleccionada


    def set_indice_dialogo(self, indice):
        self.indice_dialogo = indice

    def obtener_indice_dialogo(self):
        return self.indice_dialogo

    def dibujar_dialogo(self, inventory, personaje):

        if self.dialogo_activo:

            dialogo_ancho = 850
            dialogo_alto = -100
            dialogo_x = self.pantalla_ancho // 2 - dialogo_ancho // 2
            dialogo_y = self.pantalla_alto // 2 - dialogo_alto // 2
            inicio_texto_x = dialogo_x + 30
            inicio_texto_y = dialogo_y + 50
            keys = pygame.key.get_pressed()
            self.pantalla.blit(self.imagen_fondo_dialogo, (dialogo_x, dialogo_y))
            tiempo_actual = time.time()


            if personaje == "don diego":
                texto = self.dialogos_rojo[self.obtener_indice_dialogo()]
            elif personaje == "butanero":
                if self.obtener_dinero_dado():
                    texto = self.dialogos_rosa2[self.obtener_indice_dialogo()]

                else:
                    texto = self.dialogos_rosa[self.obtener_indice_dialogo()]

            if tiempo_actual - self.ultimo_update > self.velocidad_texto:
                if self.longitud_actual < len(texto):
                    self.longitud_actual += 1
                    self.ultimo_update = tiempo_actual

            texto_mostrado = texto[:self.longitud_actual]
            self.dibujar_frases(texto_mostrado, inicio_texto_x, inicio_texto_y)


            if personaje == "don diego":
                self.pantalla.blit(self.don_diego, (self.pantalla_ancho - 445, dialogo_y + 20))
                nombre = 'DON DIEGO'

            elif personaje == "butanero":
                self.pantalla.blit(self.butanero_jordi, (self.pantalla_ancho - 445, dialogo_y + 20))
                nombre = 'JORDI EL BUTANERO'
                if self.longitud_actual >= len(texto) and self.indice_dialogo == len(self.dialogos_rosa) - 1:

                    if not self.obtener_dinero_dado():
                        opciones = ["Dar dinero", "Mejor paso"]
                        for indice, opcion in enumerate(opciones):
                            color = (255,0,0) if indice == self.opcion_seleccionada else  self.MARRON
                            opcion_texto = self.fuente.render(opcion, True, color)
                            self.pantalla.blit(opcion_texto, (inicio_texto_x, inicio_texto_y + 50 + indice * 30))
                        if keys[pygame.K_UP]:
                            self.opcion_seleccionada = max(0, self.opcion_seleccionada - 1)
                            self.sonido_select.play()
                        if keys[pygame.K_DOWN]:
                            self.opcion_seleccionada = min(len(opciones) - 1, self.opcion_seleccionada + 1)
                            self.sonido_select.play()

                        if keys[pygame.K_x]:

                            if self.opcion_seleccionada == 0 and inventory.get_dinero():
                                self.set_opcion_seleccionada(0)
                                self.set_dinero_dado(True)
                                inventory.eliminar_dinero()

                        elif self.opcion_seleccionada == 0 and not inventory.get_dinero():
                            self.set_opcion_seleccionada(0)
                            self.set_dinero_dado(False)

                        elif self.opcion_seleccionada == 1:
                            self.set_opcion_seleccionada(1)
                            self.set_dinero_dado(False)


            texto_superficie = self.fuente.render(nombre, True, self.MARRON)
            texto_rect = texto_superficie.get_rect(center=(self.pantalla_ancho - 350, dialogo_y + 260))
            self.pantalla.blit(texto_superficie, texto_rect)

    def dibujar_frases(self, texto_mostrado, inicio_texto_x, inicio_texto_y):

        if texto_mostrado.startswith('\u200B'):
            self.sonido_letra.set_volume(1)
            self.sonido_letra.play()

        if texto_mostrado.endswith("\u00A0") or texto_mostrado.endswith("\u00A0"):
            self.sonido_letra.set_volume(0)
            self.sonido_letra.stop()


        texto_mostrado = texto_mostrado.lstrip('\u200B')
        texto_mostrado = texto_mostrado.lstrip('\u00A0')

        max_ancho_linea = 450
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
            self.pantalla.blit(self.fuente.render(linea_actual, True, self.MARRON),
                               (inicio_texto_x, inicio_texto_y + y_offset))










