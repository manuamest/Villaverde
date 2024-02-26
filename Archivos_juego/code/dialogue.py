import pygame
import time
from inventory import Inventory
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Dialogue:
    def __init__(self, inventory):

        # Pantalla
        self.pantalla_ancho = SCREEN_WIDTH
        self.pantalla_alto = SCREEN_HEIGHT
        self.pantalla = pygame.display.set_mode((self.pantalla_ancho, self.pantalla_alto))

        # Sonido diálogos
        pygame.mixer.init()
        self.sonido_letra = pygame.mixer.Sound("./code/sounds/beep.wav")
        self.sonido_select = pygame.mixer.Sound("./code/sounds/select.wav")

        # Letras
        self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)
        self.COLOR_LETRAS = (238, 212, 167)
        self.MARRON = (128, 58, 58)
        self.GRIS = (200, 200, 200)

        #Sprites Diálogos
        self.definir_sprites()

        #Diálogos personajes
        self.definir_dialogos()

        # Atributos
        self.inventory = inventory
        self.indice_dialogo = 0
        self.opcion_escogida = False
        self.opcion_seleccionada = 0
        self.dialogo_abierto = False
        self.opcion_tiene_dinero = False
        self.dinero_dado = False
        self.longitud_actual = 0
        self.update = time.time()
        self.velocidad_texto = 0.05


        

    def definir_dialogos(self):
        self.dialogos_dondiego = ["Ugh...ugh...necesito una monst...er.", "Querido Wuan, salva la granja...esta todo en tus manos.","Eres el unico capaz de hacer que me vaya de esta vida en paz...cumple solo este favor..."]
        self.dialogos_butanero = ["Hola! Soy Jordi el butanero.", "Dame el dinero!!!"]
        self.dialogos_butanero_2 = ["Wuan vamos bien, sigue asi!"]

        dialogos = [
            self.dialogos_dondiego,
            self.dialogos_butanero,
            self.dialogos_butanero_2
        ]
        
        for lista_dialogos in dialogos:
            for i in range(len(lista_dialogos)):
                lista_dialogos[i] = '\u200B' + lista_dialogos[i] + '\u00A0'


    def definir_sprites(self):
        self.imagen_fondo_dialogo = pygame.image.load('./code/sprites/dialogos/dialogue_box2.png').convert_alpha()
        self.don_diego = pygame.image.load('./code/sprites/dialogos/don_diego.png').convert_alpha()
        self.butanero_jordi = pygame.image.load('./code/sprites/dialogos/jordi_butanero.png').convert_alpha()

    def reiniciar_letras(self):

        self.longitud_actual = 0
        self.update = time.time()

    def set_opcion_dinero(self, tiene_dinero):
        self.opcion_tiene_dinero = tiene_dinero

    def set_opcion_escogida(self, opcion_escogida):
        self.opcion_escogida = opcion_escogida

    def set_opcion_dialogo(self, dialogo_abierto):
        self.dialogo_abierto = dialogo_abierto
  

    def set_dinero_dado(self, dinero_dado):
        self.dinero_dado = dinero_dado

  
    def set_opcion_seleccionada(self, opcion):
        self.opcion_seleccionada = opcion

    def set_indice_dialogo(self, indice):
        self.indice_dialogo = indice
       
    def obtener_dialogo(self):
        return self.dialogo_abierto
    
    def obtener_dinero_dado(self):
        return self.dinero_dado

    def obtener_dialogo_personaje(self, personaje):
        if personaje == "don diego":
            return self.dialogos_dondiego
        elif personaje == "butanero" and self.obtener_dinero_dado():
            return self.dialogos_butanero_2
        elif personaje == "butanero":
            return self.dialogos_butanero
        else:
            return []
        

    def manejar_interacciones(self, keys, inventory,personaje,inicio_texto_x,inicio_texto_y):
        
            if personaje == "butanero":
                self.manejar_opciones_butanero(keys, inventory,inicio_texto_x,inicio_texto_y)
           
          
    def manejar_opciones_butanero(self, keys, inventory,inicio_texto_x,inicio_texto_y):
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


    def dibujar_dialogo(self, inventory, personaje):
        if self.dialogo_abierto:
            dialogo_ancho = 850
            dialogo_alto = -100
            dialogo_x = self.pantalla_ancho // 2 - dialogo_ancho // 2
            dialogo_y = self.pantalla_alto // 2 - dialogo_alto // 2
            inicio_texto_x = dialogo_x + 30
            inicio_texto_y = dialogo_y + 50
            keys = pygame.key.get_pressed()
            self.pantalla.blit(self.imagen_fondo_dialogo, (dialogo_x, dialogo_y))
            tiempo_actual = time.time()
            
            dialogos_personaje = self.obtener_dialogo_personaje(personaje)

            if tiempo_actual - self.update > self.velocidad_texto:
                if self.longitud_actual < len(dialogos_personaje[self.indice_dialogo]):
                    self.longitud_actual += 1
                    self.update = tiempo_actual

            texto_mostrado = dialogos_personaje[self.indice_dialogo][:self.longitud_actual]
            self.dibujar_frases(texto_mostrado, inicio_texto_x, inicio_texto_y)

            personajes = {
                "don diego": (self.don_diego, 'DON DIEGO'),
                "butanero": (self.butanero_jordi, 'JORDI EL BUTANERO')
            }

            if personaje in personajes:
                imagen, nombre = personajes[personaje]
                self.pantalla.blit(imagen, (self.pantalla_ancho - 445, dialogo_y + 20))
                if personaje == "butanero" and self.longitud_actual >= len(dialogos_personaje[self.indice_dialogo]) and self.indice_dialogo == len(dialogos_personaje) - 1:
                    self.manejar_interacciones(keys, inventory, personaje, inicio_texto_x, inicio_texto_y)
            else:
                nombre = ''

            texto_superficie = self.fuente.render(nombre, True, self.MARRON)
            texto_rect = texto_superficie.get_rect(center=(self.pantalla_ancho - 350, dialogo_y + 260))
            self.pantalla.blit(texto_superficie, texto_rect)


    def dibujar_frases(self, texto_mostrado, inicio_texto_x, inicio_texto_y, max_ancho_linea=450, color_texto=None, texto_inicio_especial='\u200B', texto_fin_especial='\u00A0'):

        if texto_mostrado.startswith(texto_inicio_especial):
            self.sonido_letra.set_volume(5)
            self.sonido_letra.play()

        if texto_mostrado.endswith(texto_fin_especial):
            self.sonido_letra.set_volume(0)
            self.sonido_letra.stop()

        texto_mostrado = texto_mostrado.lstrip(texto_inicio_especial)
        texto_mostrado = texto_mostrado.lstrip(texto_fin_especial)

        palabras = texto_mostrado.split(' ')
        linea_actual = ""
        y_offset = 0

        for palabra in palabras:
            prueba_linea = f"{linea_actual} {palabra}" if linea_actual else palabra
            prueba_superficie = self.fuente.render(prueba_linea, True, color_texto if color_texto else self.MARRON)
            prueba_ancho = prueba_superficie.get_width()

            if prueba_ancho <= max_ancho_linea:
                linea_actual = prueba_linea
            else:
                self.pantalla.blit(self.fuente.render(linea_actual, True, color_texto if color_texto else self.MARRON),
                                (inicio_texto_x, inicio_texto_y + y_offset))
                y_offset += 30
                linea_actual = palabra

        if linea_actual:
            self.pantalla.blit(self.fuente.render(linea_actual, True, color_texto if color_texto else self.MARRON),
                            (inicio_texto_x, inicio_texto_y + y_offset))

            
    
    




