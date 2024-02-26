import pygame
import time
from inventory import Inventory
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Dialogue:
    def __init__(self):

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

      
        # Atributos
        self.inventory = Inventory()
        self.indice_dialogo = 0
        self.opcion_escogida = False
        self.opcion_seleccionada = 0
        self.dialogo_abierto = False
        self.material_dado = False
        self.longitud_actual = 0
        self.update = time.time()
        self.velocidad_texto = 0.05
        self.confirmacion_abierta = False
        self.valor = 0
        self.mensaje_confirmacion = ""
        self.cantidades = {"Madera": 0, "Trigo": 0}
        self.cantidad_seleccionada = 0
        self.item_seleccionado = None
        self.pago = 0
        self.material_dado = False
        self.final_dialogo = False
        self.dinero_dado = False
        self.cantidades = {
        "Madera": 0,
        "Trigo": 0,
        "Zapatillas": 0,
        "Bufandas": 0
        }

        
 

          #Sprites Diálogos
        self.definir_sprites()

        #Diálogos personajes
        self.definir_dialogos()

        self.definir_indices()


    def definir_dialogos(self):
        self.dialogos_dondiego = ["Ugh...ugh...necesito una monst...er.", "Querido Wuan, salva la granja...esta todo en tus manos.","Eres el unico capaz de hacer que me vaya de esta vida en paz...cumple solo este favor..."]
        self.dialogos_butanero = ["Hola! Soy Jordi el butanero.", "Dame el dinero!!!"]
        self.dialogos_butanero_2 = ["Wuan vamos bien, sigue asi!"]
        self.dialogos_mercader = ["Bienvenido a la tienda de Xoel el mercader, donde tu madera y trigo compra sin perder.Trae tus bienes, los frutos de tu labor, Xoel paga bien, con justicia y honor.","Dicen que soy agarrado, de mi eso murmuran,por no soltar el dinero, criticas me aseguran. Mas si supieran la verdad, detras del velo y la penumbra,necesito cada centavo, para vivir sin ninguna duda.","Dime Wuan, como te puedo estafar hoy?"]
        self.dialogos_mercader_3 = ["No puedes seleccionar 0 unidades."]
        self.dialogos_modista_3 = ["No puedes seleccionar 0 unidades querido Wuan...se paciente"]
        self.dialogos_mercader_4 = ["Es un placer hacer negocios contigo, vuelve cuando quieras!!!"]
        self.dialogos_mercader_5 = ["No tienes suficientes unidades del material, vuelve cuando las hayas conseguido"]
        self.dialogos_modista_4 = ["Es un placer hacer negocios contigo, vuelve cuando quieras!!!"]
        self.dialogos_modista_5 = ["No tienes suficiente dinero, vuelve cuando consigas mas dinero con Xoel el mercader"]
        self.dialogos_mercader_6 = ["Avisame si cambias de opinion!"]
        self.dialogos_modista_6 = ["Juntos reconstruiremos la granja!Vuelve pronto, cada poco tiempo recibo mercancia de nuevos accesorios"]
        self.dialogos_modista = ["Bienvenido a la tienda de Eva la modista...Wuan, que articulo de lujo necesitas?","Nos han llegado las ultimas novedades como las bufandas de Moo-lana, a las vacas misteriosamente les atrae este accesorio..."]
 
        dialogos = [
            self.dialogos_dondiego,
            self.dialogos_butanero,
            self.dialogos_butanero_2,
            self.dialogos_mercader,
            self.dialogos_mercader_3,
            self.dialogos_mercader_4,
            self.dialogos_mercader_5,
            self.dialogos_mercader_6,
            self.dialogos_modista_3,
            self.dialogos_modista_4,
            self.dialogos_modista_5,
            self.dialogos_modista_6,
            self.dialogos_modista
        ]
        
        for lista_dialogos in dialogos:
            for i in range(len(lista_dialogos)):
                lista_dialogos[i] = '\u200B' + lista_dialogos[i] + '\u00A0'


    def definir_sprites(self):
        self.imagen_fondo_dialogo = pygame.image.load('./code/sprites/dialogos/dialogue_box2.png').convert_alpha()
        self.imagen_menu = pygame.image.load('./code/sprites/dialogos/menu.png').convert_alpha()
        self.don_diego = pygame.image.load('./code/sprites/dialogos/don_diego.png').convert_alpha()
        self.butanero_jordi = pygame.image.load('./code/sprites/dialogos/jordi_butanero.png').convert_alpha()
        self.mercader = pygame.image.load('./code/sprites/dialogos/XoelMercader_dialogue.png').convert_alpha()
        self.modista = pygame.image.load('./code/sprites/dialogos/EvaModista_dialogue.png').convert_alpha()

    def definir_indices(self):
        # Define un diccionario para mantener los índices de diálogo de cada personaje
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
        if personaje in self.indices:
            self.indices[personaje] = indice

    def set_opcion_escogida(self, opcion_escogida):
        self.opcion_escogida = opcion_escogida

    def set_final_dialogo(self, final_dialogo):
        self.final_dialogo = final_dialogo
 
    def set_opcion_dialogo(self, dialogo_abierto):
        self.dialogo_abierto = dialogo_abierto
  

    def set_material_dado(self, material_dado):
        self.material_dado = material_dado

    
    def set_dinero_dado(self, dinero_dado):
        self.dinero_dado = dinero_dado


    def set_cantidad_seleccionada(self, cantidad_seleccionada):
        self.cantidad_seleccionada = cantidad_seleccionada
    
    def obtener_final_dialogo(self):
        return self.final_dialogo

    def set_opcion_escogida(self, opcion_escogida):
        self.opcion_escogida = opcion_escogida


    def obtener_indice_personaje(self, personaje):
        return self.indices.get(personaje, 0)
    
    def obtener_opcion_escogida(self):
        return self.opcion_escogida
      
    def obtener_cantidad_seleccionada(self):
      return self.cantidad_seleccionada
    
    def set_confirmacion_abierta(self, confirmacion_abierta):
        self.confirmacion_abierta = confirmacion_abierta
    
    def obtener_confirmacion_abierta(self):
        return self.confirmacion_abierta
    
    def obtener_dinero_dado(self):
        return self.dinero_dado

  
    def set_opcion_seleccionada(self, opcion):
        self.opcion_seleccionada = opcion

    def obtener_opcion_seleccionada(self):
       return  self.opcion_seleccionada

       
    def obtener_dialogo(self):
        return self.dialogo_abierto
    
    def obtener_material_dado(self):
        return self.material_dado

    def get_pago_mercader(self,item, cantidad):
     
        precio_madera = 5 
        precio_trigo = 3  

        if item == "Madera":
            pago_total = cantidad * precio_madera
        elif item == "Trigo":
            pago_total = cantidad * precio_trigo
        else:
            pago_total = 0  
        return pago_total
    
    def get_pago_modista(self, item, cantidad):
 
        precio_zapatillas = 10 
        precio_bufandas = 7  

        if item == "Zapatillas":
            pago_total = cantidad * precio_zapatillas
        elif item == "Bufandas":
            pago_total = cantidad * precio_bufandas
        else:
            pago_total = 0  

        return pago_total

    def obtener_dialogo_personaje(self, personaje):
        if personaje == "don diego":
            return self.dialogos_dondiego
            
        elif personaje == "butanero":
            return self.dialogos_butanero_2 if self.obtener_dinero_dado() else self.dialogos_butanero

        elif personaje == "mercader":
            if self.obtener_opcion_escogida():
                if self.obtener_opcion_seleccionada() == 1:
                    return self.dialogos_mercader_6
                elif self.obtener_opcion_seleccionada() == 0:
                    return self.dialogos_mercader_4 if self.obtener_material_dado() else self.dialogos_mercader_5
            elif self.obtener_confirmacion_abierta():
                if self.obtener_cantidad_seleccionada() == 0:
                    return self.dialogos_mercader_3
                else:
                    self.pago = self.get_pago_mercader(self.item_seleccionado, self.cantidad_seleccionada)
                    return ["\u200BSeguro que quieres vender {} unidades de {}? Te ofrecere por ello {} unidades de dinero. Hay trato?\u00A0".format(self.cantidad_seleccionada, self.item_seleccionado[0].lower() + self.item_seleccionado[1:] if self.item_seleccionado else '',self.pago)]
            else:
                return self.dialogos_mercader

        elif personaje == "modista":
            if self.obtener_opcion_escogida():
                if self.obtener_opcion_seleccionada() == 1:
                    return self.dialogos_modista_6
                elif self.obtener_opcion_seleccionada() == 0:
                    return self.dialogos_modista_4 if self.obtener_material_dado() else self.dialogos_modista_5
            elif self.obtener_confirmacion_abierta():
                if self.obtener_cantidad_seleccionada() == 0:
                    return self.dialogos_modista_3
                else:
                    self.pago = self.get_pago_modista(self.item_seleccionado, self.cantidad_seleccionada)
                    return ["\u200BSeguro que quieres comprar {} unidades de {}? Te cobrare por ello {} unidades de dinero. Es una buena oferta, verdad?\u00A0".format(self.cantidad_seleccionada, self.item_seleccionado[0].lower() + self.item_seleccionado[1:] if self.item_seleccionado else '',self.pago)]
            else:
                return self.dialogos_modista

        else:
            return []

            
          
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



    def manejar_opciones_mercader(self, keys, inventory, inicio_texto_x, inicio_texto_y):

            opciones = ["Si, quiero venderlo", "No, no me interesa"]
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

                self.set_opcion_escogida(True)
                if self.opcion_seleccionada == 0 and self.item_seleccionado == "Madera" and self.cantidad_seleccionada <= inventory.get_madera():  
                    self.set_opcion_seleccionada(0)
                    self.set_material_dado(True)
                    inventory.eliminar_madera(self.cantidad_seleccionada)
                    self.pago = self.get_pago_mercader(self.item_seleccionado,self.cantidad_seleccionada)
                    inventory.añadir_dinero_mercader(self.pago)

                elif self.opcion_seleccionada == 0 and self.item_seleccionado == "Trigo" and self.cantidad_seleccionada <= inventory.get_trigo():  
                    self.set_opcion_seleccionada(0)
                    self.set_material_dado(True)
                    inventory.eliminar_trigo(self.cantidad_seleccionada)
                    self.pago = self.get_pago_mercader(self.item_seleccionado,self.cantidad_seleccionada)
                    inventory.añadir_dinero_mercader(self.pago)

                elif self.opcion_seleccionada == 0 and self.item_seleccionado == "Madera" and self.cantidad_seleccionada >= inventory.get_madera(): 
                    self.set_opcion_seleccionada(0)
                    self.set_material_dado(False)
                
                elif self.opcion_seleccionada == 0 and self.item_seleccionado == "Madera" and self.cantidad_seleccionada >= inventory.get_trigo(): 
                    self.set_opcion_seleccionada(0)
                    self.set_material_dado(False)

                elif self.opcion_seleccionada == 1:  
                    self.set_opcion_seleccionada(1)
                    self.set_material_dado(False)

    def manejar_opciones_modista(self, keys, inventory, inicio_texto_x, inicio_texto_y):

            opciones = ["Si, quiero venderlo", "Tengo que ahorrar mas, estoy pobre"]
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

                self.set_opcion_escogida(True)
                self.pago = self.get_pago_modista(self.item_seleccionado,self.cantidad_seleccionada)
                if self.opcion_seleccionada == 0 and self.item_seleccionado == "Zapatillas" and self.pago <= inventory.get_dinero():  
                    self.set_opcion_seleccionada(0)
                    self.set_material_dado(True)
                    inventory.eliminar_dinero_modista(self.pago)
                    inventory.añadir_zapatillas()

                elif self.opcion_seleccionada == 0 and self.item_seleccionado == "Bufandas" and self.pago <= inventory.get_dinero():  
                    self.set_opcion_seleccionada(0)
                    self.set_material_dado(True)
                    inventory.eliminar_dinero_modista(self.pago)
                    inventory.añadir_bufandas()
                   

                elif self.opcion_seleccionada == 0 and self.item_seleccionado == "Zapatillas" and self.pago >= inventory.get_madera(): 
                    self.set_opcion_seleccionada(0)
                    self.set_material_dado(False)
                
                elif self.opcion_seleccionada == 0 and self.item_seleccionado == "Bufandas" and self.pago >= inventory.get_trigo(): 
                    self.set_opcion_seleccionada(0)
                    self.set_material_dado(False)

                elif self.opcion_seleccionada == 1:  
                    self.set_opcion_seleccionada(1)
                    self.set_material_dado(False)



    def manejar_interacciones(self, personaje, keys, inventory, inicio_texto_x, inicio_texto_y,longitud_actual):
        dialogos_personaje = self.obtener_dialogo_personaje(personaje)
        indice_dialogo = self.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if personaje == "butanero":
            if fin_dialogo:
                self.manejar_opciones_butanero(keys, inventory, inicio_texto_x, inicio_texto_y)

        elif personaje == "mercader":
            if self.obtener_opcion_escogida() and (self.obtener_opcion_seleccionada() in [0, 1]) and fin_dialogo and self.confirmacion_abierta:
                self.set_final_dialogo(True)
             
            elif self.obtener_cantidad_seleccionada() == 0 and self.obtener_confirmacion_abierta() and not self.obtener_opcion_escogida():
                self.dibujar_menu(personaje, inventory, keys)
            elif self.obtener_opcion_seleccionada() == 1 and self.obtener_opcion_escogida():
                self.dibujar_menu(personaje, inventory, keys)
            elif fin_dialogo and not self.confirmacion_abierta:
                self.dibujar_menu(personaje, inventory, keys)
            elif not self.obtener_opcion_escogida() and fin_dialogo and self.confirmacion_abierta:
                self.manejar_opciones_mercader(keys, inventory, inicio_texto_x, inicio_texto_y)

        elif personaje == "modista":

            if self.obtener_opcion_escogida() and (self.obtener_opcion_seleccionada() in [0, 1]) and fin_dialogo and self.confirmacion_abierta:
                self.set_final_dialogo(True)   
            elif self.obtener_cantidad_seleccionada() == 0 and self.obtener_confirmacion_abierta() and not self.obtener_opcion_escogida():
                self.dibujar_menu(personaje, inventory, keys)
            elif self.obtener_opcion_seleccionada() == 1 and self.obtener_opcion_escogida():
                self.dibujar_menu(personaje, inventory, keys)
            elif fin_dialogo and not self.confirmacion_abierta:
                self.dibujar_menu(personaje, inventory, keys)
            elif not self.obtener_opcion_escogida() and fin_dialogo and self.confirmacion_abierta:
                self.manejar_opciones_modista(keys, inventory, inicio_texto_x, inicio_texto_y)

        

    
    def dibujar_menu(self, personaje, inventory, keys):
        if not self.obtener_opcion_escogida():
            self.personaje = personaje

            # Dimensiones y posición del menú
            menu_ancho = 350
            menu_alto = 400
            menu_x = self.pantalla_ancho // 2 - menu_ancho // 2 - 400
            menu_y = self.pantalla_alto // 2 - menu_alto // 2 - 155

            if personaje == "mercader":
                opciones = ["Madera", "Trigo"]
            elif personaje == "modista":
                opciones = ["Zapatillas", "Bufandas"]
                # Asegurarse de que las opciones de la modista están en el diccionario de cantidades
                for opcion in opciones:
                    if opcion not in self.cantidades:
                        self.cantidades[opcion] = 0

            # Detectar acciones de incremento/decremento antes de dibujar el menú para asegurar la actualización en tiempo real
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RIGHT:
                        # Asumiendo que 'opcion_seleccionada' es el índice de la opción actualmente seleccionada
                        self.cantidades[opciones[self.opcion_seleccionada]] += 1
                    elif evento.key == pygame.K_LEFT and self.cantidades[opciones[self.opcion_seleccionada]] > 0:
                        self.cantidades[opciones[self.opcion_seleccionada]] -= 1

            # Dibujar el fondo del menú
            imagen_menu_escalada = pygame.transform.scale(self.imagen_menu, (menu_ancho, menu_alto))
            self.pantalla.blit(imagen_menu_escalada, (menu_x, menu_y))

            for indice, opcion in enumerate(opciones):
                color = (255, 0, 0) if indice == self.opcion_seleccionada else self.COLOR_LETRAS
                opcion_texto = self.fuente.render(f"{opcion}:  {self.cantidades[opcion]}", True, color)
                barra_x = menu_x + 50 
                barra_y = menu_y + 60 + (indice * 50)

                pygame.draw.rect(self.pantalla, (0, 0, 0), (barra_x - 20, barra_y, 280, 40), border_radius=5)
                pygame.draw.rect(self.pantalla, self.MARRON, (barra_x + 2 - 20, barra_y + 2, 276, 36), border_radius=5)
                self.pantalla.blit(opcion_texto, (barra_x + 10 - 20, barra_y + 10))

                if opcion in inventory.sprites_items:
                    sprite = inventory.sprites_items[opcion]
                    sprite_escalado = pygame.transform.scale(sprite, (36, 36))
                    sprite_x = barra_x + 240 - 20
                    self.pantalla.blit(sprite_escalado, (sprite_x, barra_y + 2))

            # Navegación del menú
            if keys[pygame.K_UP] and self.opcion_seleccionada > 0:
                self.opcion_seleccionada -= 1
                self.sonido_select.play()
            if keys[pygame.K_DOWN] and self.opcion_seleccionada < len(opciones) - 1:
                self.opcion_seleccionada += 1
                self.sonido_select.play()

            # Confirmar la selección y cantidad
            if keys[pygame.K_x]:
                self.set_confirmacion_abierta(True)
                self.item_seleccionado =(opciones[self.opcion_seleccionada])
                self.cantidad_seleccionada = (self.cantidades[self.item_seleccionado])




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
            self.dibujar_frases(texto_mostrado, inicio_texto_x, inicio_texto_y)

            personajes = {
                "don diego": (self.don_diego, 'DON DIEGO'),
                "butanero": (self.butanero_jordi, 'JORDI EL BUTANERO'),
                "mercader": (self.mercader,'XOEL EL MERCADER'),
                "modista": (self.modista, 'EVA LA MODISTA')
            }

            if personaje in personajes:
                imagen, nombre = personajes[personaje]
                self.pantalla.blit(imagen, (self.pantalla_ancho - 445, dialogo_y + 20))
                self.manejar_interacciones(personaje, keys, inventory, inicio_texto_x, inicio_texto_y,self.longitud_actual)

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
            
    def procesar_dialogo(self, keys, dialogos_personaje,timers,personaje_actual):
        if keys[pygame.K_x] and not timers['dialogo'].active:
            timers['dialogo'].activate()
            
            indice_actual = self.obtener_indice_personaje(personaje_actual)
            self.set_indice_personaje(personaje_actual, indice_actual + 1)
            self.reiniciar_letras()
            indice_actualizado = self.obtener_indice_personaje(personaje_actual)
            
            if indice_actualizado >= len(dialogos_personaje):
                if personaje_actual == "mercader" and self.obtener_confirmacion_abierta():
                    self.set_opcion_dialogo(True)
                    self.set_indice_personaje(personaje_actual, 0)

                    if self.obtener_opcion_escogida() and (self.obtener_opcion_seleccionada() == 0 or self.obtener_opcion_seleccionada() == 1):
                        self.set_opcion_dialogo(True)

                        if self.obtener_opcion_escogida():
                            if self.obtener_final_dialogo():
                                self.set_opcion_dialogo(False)
                                self.set_final_dialogo(False)
                                self.set_confirmacion_abierta(False)
                                self.set_opcion_escogida(False)
                                self.set_indice_personaje(personaje_actual, 2) 
                                self.cantidades = {"Madera": 0, "Trigo": 0,"Zapatillas":0,"Bufandas":0}
                                personaje_actual = None

                elif personaje_actual == "modista" and self.obtener_confirmacion_abierta():
                    self.set_opcion_dialogo(True)
                    self.set_indice_personaje(personaje_actual, 0)

                    if self.obtener_opcion_escogida() and (self.obtener_opcion_seleccionada() == 0 or self.obtener_opcion_seleccionada() == 1):
                        self.set_opcion_dialogo(True)

                        if self.obtener_opcion_escogida():
                            if self.obtener_final_dialogo():
                                self.set_opcion_dialogo(False)
                                self.set_final_dialogo(False)
                                self.set_confirmacion_abierta(False)
                                self.set_opcion_escogida(False)
                                self.cantidades = {"Madera": 0, "Trigo": 0,"Zapatillas": 0, "Bufandas": 0}
                                self.set_indice_personaje(personaje_actual, 1) 
                                personaje_actual = None

                elif personaje_actual == "butanero" and self.obtener_dinero_dado():
                    self.set_dinero_dado(True)
                    self.set_indice_personaje(personaje_actual, 0)
                    self.set_opcion_dialogo(False)
                    self.set_final_dialogo(False)
                    personaje_actual = None

                else:
                        self.set_opcion_dialogo(False)
                        self.set_final_dialogo(False)
                        self.set_confirmacion_abierta(False)
                        self.set_opcion_escogida(False)
                        self.set_indice_personaje(personaje_actual, 0)
                        personaje_actual = None
            

            
    
    



