import pygame
import time
from inventory import Inventory
from draw import Draw
from npcs_strategy import *
from animals_strategy import *
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Dialogue:
    def __init__(self,screen):
            

            self.pantalla = screen
            
             # Almacena el objeto screen como un atributo de la instancia
            self.pantalla_ancho = SCREEN_WIDTH
            self.pantalla_alto = SCREEN_HEIGHT
            
        
            pygame.mixer.init()
            self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)
            self.sonido_select = pygame.mixer.Sound("./code/sounds/select.wav")
            self.imagen_fondo_dialogo = pygame.image.load('./code/sprites/dialogos/dialogue_box2.png').convert_alpha()
            self.imagen_menu = pygame.image.load('./code/sprites/dialogos/menu.png').convert_alpha()
            self.don_diego = pygame.image.load('./code/sprites/dialogos/diego.png').convert_alpha()
            self.butanero_jordi = pygame.image.load('./code/sprites/dialogos/jordi.png').convert_alpha()
            self.mercader = pygame.image.load('./code/sprites/dialogos/xoel.png').convert_alpha()
            self.modista = pygame.image.load('./code/sprites/dialogos/eva.png').convert_alpha()
            self.pollo = pygame.image.load('./code/sprites/dialogos/dialogo_pollo.png').convert_alpha()
            self.oveja = pygame.image.load('./code/sprites/dialogos/dialogo_oveja.png').convert_alpha()
            self.vaca =  pygame.image.load('./code/sprites/dialogos/dialogo_vaca.png').convert_alpha()
            self.pablo = pygame.image.load('./code/sprites/dialogos/pablo_manu.png').convert_alpha()
            self.manu = pygame.image.load('./code/sprites/dialogos/pablo_manu.png').convert_alpha()
            self.COLOR_LETRAS = (238, 212, 167)
            self.MARRON = (128, 58, 58)
            self.GRIS = (200, 200, 200)

            self.inventory = Inventory(screen)
            self.draw = Draw(screen)
        
            self.draw.definir_dialogos()
            self.inicializar_atributos()

       
    def inicializar_atributos(self):
        
        self.opcion_escogida = False
        self.opcion_escogida_vaca = False
        self.opcion_escogida_pollo = False
        self.opcion_escogida_oveja = False
        self.opcion_seleccionada = 0
        self.opcion_seleccionada_oveja = 0
        self.opcion_seleccionada_vaca = 0
        self.opcion_seleccionada_pollo = 0
        self.cantidad_seleccionada = 0
        self.dialogo_abierto = False
        self.material_dado = False
        self.longitud_actual = 0
        self.update = time.time()
        self.velocidad_texto = 0.03
        self.confirmacion_abierta = False 
        self.todo_vendido = 0
        self.final_dialogo = False
        self.dinero_dado = False
        self.gafas_dadas = False
        self.jordan_dadas = False
        self.bufandas_dadas = False
        self.jordan_compradas = False
        self.gafas_compradas = False
        self.bufandas_compradas = False
        self.todo_vendido = False
        self.madera_dada = False
        self.contador_llave = 0
        self.opcion_escogida_butanero = False
        self.estrategias_dialogo = {
            "don diego": DialogoDonDiegoEstrategia(self.draw),
            "butanero": DialogoButaneroEstrategia(self.draw),
            "hermanos": DialogoHermanosEstrategia(self.draw),
            "mercader": DialogoMercaderEstrategia(self.draw),
            "modista": DialogoModistaEstrategia(self.draw),
            "pollo": DialogoPolloEstrategia(self.draw),
            "vaca": DialogoVacaEstrategia(self.draw),
            "oveja": DialogoOvejaEstrategia(self.draw),
        }

    
        self.valor = 0
        self.cantidades = {
            "Madera": 0,
            "Trigo": 0,
            "Jordan": 0,
            "Bufanda y boina": 0,
            "Gafas y cadena":0
        }

        self.precios = {
            "mercader": {"Madera": 5, "Trigo": 3},
            "modista": {"Jordan": 10, "Bufanda y boina": 7,"Gafas y cadena":5}
        }

        self.indices = {
            "don diego": 0,
            "butanero": 0,
            "mercader": 0,
            "modista": 0,
        }
     
   

    def reiniciar_letras(self):

        self.longitud_actual = 0
        self.update = time.time()


    def set_indice_personaje(self, personaje, indice):
        self.indices[personaje] = indice

    def obtener_indice_personaje(self, personaje):
        return self.indices.get(personaje, 0)

    def set_opcion_escogida(self, opcion_escogida):
        self.opcion_escogida = opcion_escogida

    def obtener_opcion_escogida(self):
        return self.opcion_escogida
    

    def set_madera_dada(self, madera_dada):
        self.madera_dada = madera_dada

    def obtener_madera_dada(self):
        return self.madera_dada
    
    def set_opcion_escogida_butanero(self, opcion_escogida_butanero):
        self.opcion_escogida_butanero = opcion_escogida_butanero

    def obtener_opcion_escogida_butanero(self):
        return self.opcion_escogida_butanero
    
    
    def set_opcion_escogida_pollo(self, opcion_escogida_pollo):
        self.opcion_escogida_pollo = opcion_escogida_pollo

    def obtener_opcion_escogida_pollo(self):
        return self.opcion_escogida_pollo
    
    def set_opcion_escogida_oveja(self, opcion_escogida_oveja):
        self.opcion_escogida_oveja = opcion_escogida_oveja

    def obtener_opcion_escogida_oveja(self):
        return self.opcion_escogida_oveja

    
    def set_opcion_escogida_vaca(self, opcion_escogida_vaca):
        self.opcion_escogida_vaca = opcion_escogida_vaca

    def obtener_opcion_escogida_vaca(self):
        return self.opcion_escogida_vaca

    def set_final_dialogo(self, final_dialogo):
        self.final_dialogo = final_dialogo

    def obtener_final_dialogo(self):
        return self.final_dialogo
    

    def set_gafas_dadas(self, gafas_dadas):
        self.gafas_dadas = gafas_dadas

    def get_gafas_dadas(self):
        return self.gafas_dadas
    

    def set_jordan_dadas(self, jordan_dadas):
        self.jordan_dadas = jordan_dadas

    def get_jordan_dadas(self):
        return self.jordan_dadas
    
    def set_bufandas_dadas(self, bufandas_dadas):
        self.bufandas_dadas = bufandas_dadas

    def get_bufandas_dadas(self):
        return self.bufandas_dadas

    def set_opcion_dialogo(self, dialogo_abierto):
        self.dialogo_abierto = dialogo_abierto

    def obtener_dialogo(self):
        return self.dialogo_abierto

    def set_material_dado(self, material_dado):
        self.material_dado = material_dado

    def obtener_material_dado(self):
        return self.material_dado

    def set_dinero_dado(self, dinero_dado):
        self.dinero_dado = dinero_dado

    def obtener_dinero_dado(self):
        return self.dinero_dado

    def set_cantidad_seleccionada(self, cantidad_seleccionada):
        self.cantidad_seleccionada = cantidad_seleccionada

    def obtener_cantidad_seleccionada(self):
        return self.cantidad_seleccionada
    def obtener_item_seleccionado(self):
        return self.item_seleccionado


    def set_confirmacion_abierta(self, confirmacion_abierta):
        self.confirmacion_abierta = confirmacion_abierta

    def obtener_confirmacion_abierta(self):
        return self.confirmacion_abierta

    def set_opcion_seleccionada(self, opcion):
        self.opcion_seleccionada = opcion

    def obtener_opcion_seleccionada(self):
        return self.opcion_seleccionada
    

    def set_opcion_seleccionada_oveja(self, opcion):
        self.opcion_seleccionada_oveja = opcion

    def obtener_opcion_seleccionada_oveja(self):
        return self.opcion_seleccionada_oveja
    

    def set_opcion_seleccionada_vaca(self, opcion):
        self.opcion_seleccionada_vaca = opcion

    def obtener_opcion_seleccionada_vaca(self):
        return self.opcion_seleccionada_vaca
    

    def set_opcion_seleccionada_pollo(self, opcion):
        self.opcion_seleccionada_pollo = opcion

    def obtener_opcion_seleccionada_pollo(self):
        return self.opcion_seleccionada_pollo

    def calcular_pago(self, servicio, item, cantidad):
        precio = self.precios.get(servicio, {}).get(item, 0)
        return precio * cantidad
    
    def set_incr_llave(self,contador):

        self.contador_llave += contador
    
    def get_contador_llave(self):
        return self.contador_llave



    def dibujar_dialogo(self, inventory, personaje):
        if self.dialogo_abierto:
            dialogo_ancho = 850
            dialogo_alto = -100
            dialogo_x = self.pantalla_ancho // 2 - dialogo_ancho // 2
            dialogo_y = self.pantalla_alto // 2 - dialogo_alto // 2
            inicio_texto_x = dialogo_x + 30
            inicio_texto_y = dialogo_y + 50
            keys = pygame.key.get_pressed()
            indice_dialogo_actual = self.obtener_indice_personaje(personaje)
            dialogos_personaje = self.obtener_dialogo_personaje(personaje)
            self.pantalla.blit(self.imagen_fondo_dialogo, (dialogo_x, dialogo_y))
            tiempo_actual = time.time()

            if tiempo_actual - self.update > self.velocidad_texto:
                if self.longitud_actual < len(dialogos_personaje[indice_dialogo_actual]):
                    self.longitud_actual += 1
                    self.update = tiempo_actual

            texto_mostrado = dialogos_personaje[indice_dialogo_actual][:self.longitud_actual]
            self.draw.dibujar_frases(texto_mostrado, inicio_texto_x, inicio_texto_y)

            personajes = {
                "don diego": (self.don_diego, 'DON DIEGO'),
                "butanero": (self.butanero_jordi, 'JORDI EL BUTANERO'),
                "mercader": (self.mercader,'XOEL EL MERCADER'),
                "modista": (self.modista, 'EVA LA MODISTA'),
                "pollo": (self.pollo,'GALLINA DANIEL'),
                "vaca":(self.vaca,'VACA ISABEL'),
                "oveja":(self.oveja,'OVEJA OSCAR'),
                "hermanos": (self.manu,'HERMANO MANU') if self.obtener_indice_personaje(personaje) % 2 == 0 else (self.pablo,'HERMANO PABLO')

            }

            if personaje in personajes:
                imagen, nombre = personajes[personaje]
                self.pantalla.blit(imagen, (self.pantalla_ancho - 445, dialogo_y + 25))
                self.manejar_interacciones(personaje, keys, inventory, inicio_texto_x, inicio_texto_y,self.longitud_actual)

            else:
                nombre = ''

            texto_superficie = self.fuente.render(nombre, True, self.MARRON)
            texto_rect = texto_superficie.get_rect(center=(self.pantalla_ancho - 350, dialogo_y + 260))
            self.pantalla.blit(texto_superficie, texto_rect)



    def dibujar_menu(self, personaje, inventory, keys):

        if not self.obtener_opcion_escogida():   
            opciones = {"mercader": ["Madera", "Trigo"], "modista": ["Jordan", "Bufanda y boina","Gafas y cadena"]}.get(personaje, [])
            self.cantidades = {opcion: self.cantidades.get(opcion, 0) for opcion in opciones}
            menu_ancho, menu_alto = 350, 400
            menu_x, menu_y = self.pantalla_ancho // 2 - menu_ancho // 2 - 400, self.pantalla_alto // 2 - menu_alto // 2 - 155
            self.pantalla.blit(pygame.transform.scale(self.imagen_menu, (menu_ancho, menu_alto)), (menu_x, menu_y))

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RIGHT:
                        if personaje == "modista":
                            self.cantidades[opciones[self.opcion_seleccionada]] = min(self.cantidades[opciones[self.opcion_seleccionada]] + 1, 1)  
                        else:
                            self.cantidades[opciones[self.opcion_seleccionada]] += 1  
                    elif evento.key == pygame.K_LEFT and self.cantidades[opciones[self.opcion_seleccionada]] > 0:
                        self.cantidades[opciones[self.opcion_seleccionada]] -= 1

            for indice, opcion in enumerate(opciones):
                color = (255, 0, 0) if indice == self.opcion_seleccionada else self.COLOR_LETRAS
                opcion_texto = self.fuente.render(f"{opcion}: {self.cantidades[opcion]}", True, color)
                barra_x, barra_y = menu_x + 50, menu_y + 60 + (indice * 50)

                pygame.draw.rect(self.pantalla, (0, 0, 0), (barra_x - 20, barra_y, 280, 40), border_radius=5)
                pygame.draw.rect(self.pantalla, self.MARRON, (barra_x + 2 - 20, barra_y + 2, 276, 36), border_radius=5)
                self.pantalla.blit(opcion_texto, (barra_x + 10 - 20, barra_y + 10))

                if opcion in inventory.sprites_items:
                    sprite_escalado = pygame.transform.scale(inventory.sprites_items[opcion], (36, 36))
                    self.pantalla.blit(sprite_escalado, (barra_x + 240 - 20, barra_y + 2))

            self.opcion_seleccionada += keys[pygame.K_DOWN] - keys[pygame.K_UP]
            self.opcion_seleccionada = max(0, min(self.opcion_seleccionada, len(opciones) - 1))
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.sonido_select.play()

            if keys[pygame.K_x]:
                self.set_confirmacion_abierta(True)
                self.item_seleccionado = opciones[self.opcion_seleccionada]
                self.cantidad_seleccionada = self.cantidades[self.item_seleccionado]

    
    def obtener_dialogo_personaje(self, personaje):
            estrategia = self.estrategias_dialogo.get(personaje)
            if estrategia:
                return estrategia.obtener_dialogo(self)
            else:
                return []
            
    def manejar_opciones_personaje(self, keys, inventory, inicio_texto_x, inicio_texto_y, personaje):
        estrategia = self.estrategias_dialogo.get(personaje)
        if estrategia:
            opciones = estrategia.manejar_opciones(self)

            for indice, opcion in enumerate(opciones):
                color = (255, 0, 0) if indice == self.opcion_seleccionada else self.MARRON
                opcion_texto = self.fuente.render(opcion, True, color)
                self.pantalla.blit(opcion_texto, (inicio_texto_x, inicio_texto_y + 110 + indice * 30))
                
            if keys[pygame.K_UP] and self.opcion_seleccionada > 0:
                self.opcion_seleccionada -= 1
                self.sonido_select.play()
            if keys[pygame.K_DOWN] and self.opcion_seleccionada < len(opciones) - 1:
                self.opcion_seleccionada += 1
                self.sonido_select.play()

            if keys[pygame.K_x]:
                    estrategia.ejecutar_accion(inventory,self, personaje)
                        
        else:
            print("No hay estrategia definida para este personaje.")


    def manejar_interacciones(self, personaje, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual):
        estrategia = self.estrategias_dialogo.get(personaje)
        if estrategia:
            estrategia.manejar_interacciones(keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje,self)
        else:
            print("No hay estrategia definida para este personaje.")


    def procesar_dialogo(self, keys, dialogos_personaje, timers, personaje_actual):
        if keys[pygame.K_x] and not timers['dialogo'].active and self.draw.caracter_especial_dibujado:
            timers['dialogo'].activate()
            indice_actual = self.obtener_indice_personaje(personaje_actual)
            self.set_indice_personaje(personaje_actual, indice_actual + 1)
            self.reiniciar_letras()
            indice_actualizado = self.obtener_indice_personaje(personaje_actual)

            if indice_actualizado >= len(dialogos_personaje):
                estrategia = self.estrategias_dialogo.get(personaje_actual)
                if estrategia:
                    estrategia.reset_dialogo(keys, dialogos_personaje,timers,personaje_actual,self)  
              
                else:
                    pass
   

