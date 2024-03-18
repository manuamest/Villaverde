import pygame
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Draw:
    def __init__(self,screen,dialogue,escene):
      self.dialogue = dialogue
      self.escene = escene
      self.pantalla = screen
      self.pantalla_ancho = SCREEN_WIDTH
      self.pantalla_alto = SCREEN_HEIGHT
      self.opcion_menu = 0

      # Fuente
      self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)
      self.MARRON = (128, 58, 58)
      self.COLOR_LETRAS = (238, 212, 167)

      # Sonidos
      self.sonido_llaves = pygame.mixer.Sound("./code/sounds/llaves.wav")
      self.sonido_select = pygame.mixer.Sound("./code/sounds/select.wav")

      # Imágenes
      self.imagen_cartel = pygame.image.load('./code/sprites/tutorial/tutorial_sin_z.png').convert_alpha()
      self.imagen_fondo_dialogo = pygame.image.load('./code/sprites/dialogos/dialogue_box2.png').convert_alpha()
      self.imagen_menu = pygame.image.load('./code/sprites/dialogos/menu.png').convert_alpha()
      self.don_diego = pygame.image.load('./code/sprites/dialogos/diego.png').convert_alpha()
      self.obrero_jordi = pygame.image.load('./code/sprites/dialogos/jordi.png').convert_alpha()
      self.mercader = pygame.image.load('./code/sprites/dialogos/xoel.png').convert_alpha()
      self.modista = pygame.image.load('./code/sprites/dialogos/eva.png').convert_alpha()
      self.pollo = pygame.image.load('./code/sprites/dialogos/dialogo_pollo.png').convert_alpha()
      self.oveja = pygame.image.load('./code/sprites/dialogos/dialogo_oveja.png').convert_alpha()
      self.cabra = pygame.image.load('./code/sprites/dialogos/oscar_dialogo.png').convert_alpha()
      self.vaca =  pygame.image.load('./code/sprites/dialogos/dialogo_vaca.png').convert_alpha()
      self.pablo = pygame.image.load('./code/sprites/dialogos/pablo_manu.png').convert_alpha()
      self.manu = pygame.image.load('./code/sprites/dialogos/pablo_manu.png').convert_alpha()
      self.moneda = pygame.image.load('./code/sprites/moneda_tiendas.png').convert_alpha()
      self.moneda2 = pygame.image.load('./code/sprites/moneda_tiendas2.png').convert_alpha()
      self.moneda3 = pygame.image.load('./code/sprites/moneda_tiendas3.png').convert_alpha()

      # Atributos
      self.cantidad_seleccionada = 0
      self.caracter_especial_dibujado = False
      self.update = time.time()
      self.longitud_actual = 0
      self.cartel_procesado = False
      self.cartel_active = False
      self.retraso_navegacion = 0 
      self.marcador= '\u00A0' 
      self.message = "Parece que para entrar aqui se necesita la Llave Magistral" 
      self.precios = {
            "mercader": {"Madera": 3, "Trigo": 5},
            "modista": {"Jordan": 33, "Bufanda y boina": 66,"Gafas y cadena":99}
        }
      
      self.definir_dialogos()

    # Reinicio de letras en el diálogo
    def reiniciar_letras(self):
        self.longitud_actual = 0
        self.update = time.time()

    # Métodos para las cantidades seleccionadas en las tiendas
    def obtener_cantidad_seleccionada(self):
        return self.cantidad_seleccionada

    def obtener_item_seleccionado(self):
        return self.item_seleccionado

    def set_cantidad_seleccionada(self, cantidad_seleccionada):
        self.cantidad_seleccionada = cantidad_seleccionada

    def set_opcion_menu(self, opcion):
        self.opcion_menu = opcion

    # Diálogos del videojuego
    def definir_dialogos(self):
        self.dialogos_dondiego  = ["Que va a ser de mi?, mi granja esta destrozada y Fer ha desaparecido...", "Por favor, Wuan, coge la bolsa que tengo en casa con todos mis ahorros y habla con Jordi el obrero, el quizas nos pueda ayudar.", "Todo esta en tus manos..."]
        self.dialogos_dondiego_2 = ["Ugh...ugh...necesito una monst...er.", "Querido Wuan, salva la granja...esta todo en tus manos.", "Eres el unico capaz de hacer que me vaya de esta vida en paz...cumple solo este favor..."]
        self.dialogos_obrero = ["Hola! Soy Jordi el obrero, yo te puedo ayudar a reconstruir la granja.", "Wuan, lamento decirte que los ahorros de tu abuelo probablemente no sean suficientes para pagar la reconstruccion...", "Si no puedes conseguir mas dinero vas a tener que proporcionarme los materiales de construccion.", "Traeme 30 de madera y 100 monedas y vere que puedo hacer."]
        self.dialogos_obrero_2 = ["Genial! Ya era hora de que por fin me trajeras el dinero y la madera, sigue asi Wuan."]
        self.dialogos_obrero_3 = ["Estas sordo primo? Que te he dicho que me des el dinero y la madera, ya veo que no tienes suficientes unidades de ambos, traeme lo que te he pedido."]
        self.dialogos_obrero_4 = ["Me vas a tener esperando un tiempecito parece eh, avisame cuando los consigas."]
        self.dialogos_obrero_5 = ["Solo tienes madera, traeme el dinero tambien anda."]
        self.dialogos_obrero_6 = ["Solo tienes dinero, traeme la madera tambien anda."]
        self.dialogos_obrero_7 = ["No tienes suficientes unidades de dinero y madera, vuelve cuando tengas la cantidad que te pedi."]
        self.dialogos_mercader = ["Bienvenido a la tienda de Xoel el mercader, donde tu madera y trigo compra sin perder. Trae tus bienes, los frutos de tu labor, Xoel paga bien, con justicia y honor.", "Dicen que soy agarrado, de mi eso murmuran, por no soltar el dinero, criticas me aseguran. Mas si supieran la verdad, detras del velo y la penumbra, necesito cada centavo, para vivir sin ninguna duda.", "Dime Wuan, como te puedo estafar hoy?"]
        self.dialogos_mercader_3 = ["No puedes seleccionar 0 unidades."]
        self.dialogos_modista_3 = ["No puedes seleccionar 0 unidades querido Wuan...se paciente."]
        self.dialogos_mercader_4 = ["Es un placer hacer negocios contigo, vuelve cuando quieras!"]
        self.dialogos_mercader_5 = ["No tienes suficientes unidades del material, vuelve cuando tengas algo que ofrecerme."]
        self.dialogos_modista_4 = ["Es un placer hacer negocios contigo, vuelve cuando quieras!"]
        self.dialogos_modista_5 = ["No tienes suficiente dinero, vuelve cuando consigas mas dinero con Xoel el mercader."]
        self.dialogos_mercader_6 = ["Avisame si cambias de opinion!"]
        self.dialogos_mercader_7 = ["Parece que todo se termina aqui...me has descubierto, no eres tan despistado como pensaba","Malditos animales, se han revelado todos, pense que podria quedarme con la granja..."]
        self.dialogos_modista_7 = ["Lo siento Wuan, no nos quedan existencias de ese articulo...era una edicion limitada."]
        self.dialogos_modista_8 = ["Madre mia Wuan, has agotado las existencias de todos mis articulos, tendre que cerrar durante un tiempo para poder reponer la mercancia!"]
        self.dialogos_modista_6 = ["Juntos reconstruiremos la granja! Vuelve pronto, seguro que ves algo que te pueda servir."]
        self.dialogos_modista = ["Bienvenido a la tienda de Eva la modista...Wuan, que articulo de lujo necesitas?", "Nos han llegado las ultimas novedades como las bufandas de Ovejana, a las ovejas misteriosamente les atrae este accesorio..."]
        self.dialogos_pollo = ["Cococo! Escucha bien, te lo voy a decir, mi amor por las Jordans es algo que no puede huir, si quieres que camine junto a ti, en este lugar, necesitas comprender que es lo que quiero calzar.", "Con mis Jordan en mis patas, contigo voy a marchar.", "Dime Wuan, me has traido mi complemento favorito? Tengo muchas ganas de lucirlas por el corral."]
        self.dialogos_pollo_2 = ["Con Jordan en las garras, sere el gallo de las carreras, Gallina Daniel, ¡brillando como estrellas en las praderas! En la granja, sere el mas veloz de todas las bestias granjeras!,Y junto a Wuan, la granja salvare, en cada paso que de!"]
        self.dialogos_pollo_3 = ["Aun no tienes mis preciadas Jordan...ya se que estan caras pero sin mi no podras conseguirlo, tu veras Wuan, o Jordans o no hay trato."]
        self.dialogos_pollo_4 = ["Que paciencia hay que tener contigo Wuan, bueno, confio en que al menos las que me traeras seran una edicion limitada."]
        self.dialogos_oveja = ["Baa-baa! Yo soy Oscar, lanuda y noble oveja, para salvar tu granja, una peticion te dejo. Una bufanda de Ovejana, con nudos de esperanza, traeme esa prenda, y juntos tendremos bonanza. Con la bufanda al cuello, sere tu fiel aliado,te ayudare en tu granja, hasta que todo haya acabado.", "Asi que amigo del campo, ya sabes mi condicion,una bufanda para mi, y yo te doy mi devocion. Juntos enfrentaremos, el frio y la adversidad,y con bufanda en mano, la granja vamos a salvar.", "Me has traido mi preciada bufanda de Ovejana?"]
        self.dialogos_oveja_2 = ["Que bien me va a sentar esta bufanda!"]
        self.dialogos_oveja_3 = ["Corre Wuan, aunque sea una oveja me estoy muriendo de frio, necesito una bufanda al cuello para poder servirte como aliado."]
        self.dialogos_oveja_4 = ["Vaya...bueno no te preocupes Wuan, confiamos todo el pueblo de Villaverde en ti, seguro que seras capaz de conseguir cada uno de los retos, aqui te esperare."]
        self.dialogos_vaca = ["Moo-moo! Presta atencion, aqui te voy a contar, mis gustos son exclusivos! Si quieres que camine a tu lado, que te siga sin fallar, necesitas comprender lo que me hace deslumbrar.", "Mi estilo ha de resplandecer, con unas gafas Swarovski, me vas a enloquecer! Asi que si quieres mi amistad, si quieres mi devocion, trae esas gafas!", "Dime cielo, tienes unas gafas rechulonas por ahi que poder darme?"]
        self.dialogos_vaca_2 = ["Gracias cielo, ahora junto a ti desfilare, con estas gafas y nuestro esfuerzo salvaremos la granja. Puedes contar conmigo, Klara, como tu fiel aliada."]
        self.dialogos_vaca_3 = ["Aun no tienes las gafas cielo...vuelve cuando tengas algo mas de disposicion."]
        self.dialogos_vaca_4 = ["De acuerdo, cuando las traigas sere la vaca mas guapa y te podre ayudar."]
        self.dialogos_hermanos = ["Al viejo ese le quedan dos telediarios.", "Con el disgusto que le ha dado Wuan, no creo que llegue a ver el amanecer.", "Wuan, eres la oveja negra de la familia.", "Espabila Wuan!", "Wuan, no tienes nada mejor que hacer?", "Wuan, tienes mucho que aprender de nosotros...", "Lavate o algo, Wuan, hueles a estiercol!"]
        self.dialogos_llave_magistral = ["Nos has reclutado a todos, por eso hemos decidido darte la Llave Magistral, ponla a buen recaudo, la necesitaras."]
        self.dialogos_cabra = ["MEEEEEEE!!!"]

        dialogos = [
            self.dialogos_dondiego,self.dialogos_dondiego_2, self.dialogos_obrero, self.dialogos_obrero_2, self.dialogos_mercader,
            self.dialogos_mercader_3, self.dialogos_mercader_4, self.dialogos_mercader_5, self.dialogos_mercader_6,self.dialogos_mercader_7,
            self.dialogos_modista_3, self.dialogos_modista_4, self.dialogos_modista_5, self.dialogos_modista_6,
            self.dialogos_modista, self.dialogos_pollo, self.dialogos_pollo_2, self.dialogos_pollo_3,
            self.dialogos_pollo_4, self.dialogos_vaca, self.dialogos_oveja, self.dialogos_oveja_2,
            self.dialogos_oveja_3, self.dialogos_oveja_4, self.dialogos_hermanos, self.dialogos_vaca_2,
            self.dialogos_vaca_3, self.dialogos_vaca_4, self.dialogos_llave_magistral, self.dialogos_modista_7,
            self.dialogos_modista_8, self.dialogos_obrero_3, self.dialogos_obrero_4, self.dialogos_obrero_5,
            self.dialogos_obrero_6, self.dialogos_obrero_7,self.dialogos_cabra
        ]

        for lista_dialogos in dialogos:
                for i in range(len(lista_dialogos)):
                    lista_dialogos[i] = lista_dialogos[i] + self.marcador
                    
    # Función para dibujar el diálogo con los personajes
    def dibujar_dialogo(self, inventory, personaje):
        if self.dialogue.dialogo_abierto:
            dialogo_ancho = 850
            dialogo_alto = -100
            dialogo_x = self.pantalla_ancho // 2 - dialogo_ancho // 2
            dialogo_y = self.pantalla_alto // 2 - dialogo_alto // 2
            inicio_texto_x = dialogo_x + 30
            inicio_texto_y = dialogo_y + 50
            keys = pygame.key.get_pressed()
            indice_dialogo_actual = self.dialogue.obtener_indice_personaje(personaje)
            dialogos_personaje = self.dialogue.obtener_dialogo_personaje(personaje)

            if 0 <= indice_dialogo_actual < len(dialogos_personaje):
                self.pantalla.blit(self.imagen_fondo_dialogo, (dialogo_x, dialogo_y))
                tiempo_actual = time.time()

                if keys[pygame.K_SPACE]:  
                    self.longitud_actual = len(dialogos_personaje[indice_dialogo_actual])
                elif tiempo_actual - self.update > 0.05:
                    if self.longitud_actual < len(dialogos_personaje[indice_dialogo_actual]):
                        self.longitud_actual += 1
                        self.update = tiempo_actual

                texto_mostrado = dialogos_personaje[indice_dialogo_actual][:self.longitud_actual]
                self.dibujar_frases(texto_mostrado, inicio_texto_x, inicio_texto_y)
                
                personajes = {
                    "don diego": (self.don_diego, 'DON DIEGO'),
                    "obrero": (self.obrero_jordi, 'JORDI EL OBRERO'),
                    "mercader": (self.mercader,'XOEL EL MERCADER'),
                    "modista": (self.modista, 'EVA LA MODISTA'),
                    "pollo": (self.pollo,'GALLINA DANIEL'),
                    "vaca":(self.vaca,'VACA KLARA'),
                    "oveja":(self.oveja,'OVEJA OSCAR'),
                    "cabra":(self.cabra,'CABRA FER'),
                    "hermanos": (self.manu,'HERMANO PABLO') if self.dialogue.obtener_indice_personaje(personaje) % 2 == 0 else (self.pablo,'HERMANO MANUEL')
                }

                if personaje in personajes:
                    imagen, nombre = personajes[personaje]
                    self.pantalla.blit(imagen, (self.pantalla_ancho - 445, dialogo_y + 25))
                    self.dialogue.manejar_interacciones(personaje, keys, inventory, inicio_texto_x, inicio_texto_y, self.longitud_actual)
                else:
                    nombre = ''

                texto_superficie = self.fuente.render(nombre, True, self.MARRON)
                texto_rect = texto_superficie.get_rect(center=(self.pantalla_ancho - 350, dialogo_y + 260))
                self.pantalla.blit(texto_superficie, texto_rect)

    # Función para dibujar el menú de las tiendas
    def dibujar_menu(self, personaje, inventory, keys):
        if not self.dialogue.obtener_opcion_escogida(): 
            opciones = {"mercader": ["Madera", "Trigo"], "modista": ["Jordan", "Bufanda y boina","Gafas y cadena"]}.get(personaje, [])
            self.dialogue.cantidades = {opcion: self.dialogue.cantidades.get(opcion, 0) for opcion in opciones}
            menu_ancho, menu_alto = 350, 400
            menu_x, menu_y = self.pantalla_ancho // 2 - menu_ancho // 2 - 400, self.pantalla_alto // 2 - menu_alto // 2 - 155
            self.pantalla.blit(pygame.transform.scale(self.imagen_menu, (menu_ancho, menu_alto)), (menu_x, menu_y))

            for evento in pygame.event.get():
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RIGHT:
                            if personaje == "modista":
                                cantidad_anterior = self.dialogue.cantidades[opciones[self.opcion_menu]]
                                self.dialogue.cantidades[opciones[self.opcion_menu]] = min(cantidad_anterior + 1, 1)  
                                if cantidad_anterior != self.dialogue.cantidades[opciones[self.opcion_menu]]:
                                    self.sonido_select.play()  
                            else:
                                cantidad_anterior = self.dialogue.cantidades[opciones[self.opcion_menu]]
                                self.dialogue.cantidades[opciones[self.opcion_menu]] += 1  
                                if cantidad_anterior != self.dialogue.cantidades[opciones[self.opcion_menu]]:
                                    self.sonido_select.play()  
                        elif evento.key == pygame.K_LEFT and self.dialogue.cantidades[opciones[self.opcion_menu]] > 0:
                            cantidad_anterior = self.dialogue.cantidades[opciones[self.opcion_menu]]
                            self.dialogue.cantidades[opciones[self.opcion_menu]] -= 1
                            if cantidad_anterior != self.dialogue.cantidades[opciones[self.opcion_menu]]:
                                self.sonido_select.play()  

            if keys[pygame.K_UP] and self.opcion_menu > 0:
                if self.retraso_navegacion == 0:
                    self.opcion_menu -= 1
                    self.retraso_navegacion = 10  
                    self.sonido_select.play() 
                    self.dialogue.cantidades[opciones[self.opcion_menu + 1]] = 0
                    
            elif keys[pygame.K_DOWN] and self.opcion_menu < len(opciones) - 1:
                if self.retraso_navegacion == 0:
                    self.opcion_menu += 1
                    self.retraso_navegacion = 10 
                    self.sonido_select.play() 
                    self.dialogue.cantidades[opciones[self.opcion_menu - 1]] = 0
            
            if self.retraso_navegacion > 0:
                self.retraso_navegacion -= 1

            for indice, opcion in enumerate(opciones):
                color = (255, 0, 0) if indice == self.opcion_menu else self.COLOR_LETRAS
                opcion_texto = self.fuente.render(f"{opcion}: {self.dialogue.cantidades[opcion]}", True, color)
                barra_x, barra_y = menu_x + 50, menu_y + 60 + (indice * 50)

                pygame.draw.rect(self.pantalla, (0, 0, 0), (barra_x - 20, barra_y, 280, 40), border_radius=5)
                pygame.draw.rect(self.pantalla, (177, 75, 1), (barra_x + 2 - 20, barra_y + 2, 276, 36), border_radius=5)
                self.pantalla.blit(opcion_texto, (barra_x + 10 - 20, barra_y + 10))
                texto_ancho = opcion_texto.get_width()
                posicion_moneda_x = barra_x + 10 - 20 + texto_ancho + 5 
                posicion_moneda_y = barra_y + 20
                if personaje == "modista":
                    if indice == 0:
                        moneda_a_usar = self.moneda
                    elif indice == 1:
                        moneda_a_usar = self.moneda2
                    elif indice == 2:
                        moneda_a_usar = self.moneda3
                 
                    ancho_original, alto_original = moneda_a_usar.get_size()
                    ancho_nuevo = int(ancho_original * 1.2)
                    alto_nuevo = int(alto_original * 1.2)
                    moneda_escalada = pygame.transform.scale(moneda_a_usar, (ancho_nuevo, alto_nuevo))
                    self.pantalla.blit(moneda_escalada, (posicion_moneda_x, posicion_moneda_y))
                if opcion in inventory.sprites_items:
                    sprite_escalado = pygame.transform.scale(inventory.sprites_items[opcion], (36, 36))
                    self.pantalla.blit(sprite_escalado, (barra_x + 240 - 20, barra_y + 2))

            if keys[pygame.K_x]:
                self.dialogue.set_confirmacion_abierta(True)
                self.item_seleccionado = opciones[self.opcion_menu]
                self.cantidad_seleccionada = self.dialogue.cantidades[self.item_seleccionado]
        else:
            self.opcion_menu = 0
            self.item_seleccionado = 0

    # Función para poder avanzar los diálogos
    def procesar_dialogo(self, keys, dialogos_personaje, timers, personaje_actual):
        if keys[pygame.K_x] and not timers['dialogo'].active and self.caracter_especial_dibujado:
            timers['dialogo'].activate()
            indice_actual = self.dialogue.obtener_indice_personaje(personaje_actual)
            self.dialogue.set_indice_personaje(personaje_actual, indice_actual + 1)
            self.reiniciar_letras()
            indice_actualizado = self.dialogue.obtener_indice_personaje(personaje_actual)

            if indice_actualizado >= len(dialogos_personaje):
                estrategia = self.dialogue.estrategias_dialogo.get(personaje_actual)
                if estrategia:
                    estrategia.reset_dialogo(keys, dialogos_personaje,timers,personaje_actual,self.dialogue,self.escene,self)  
                else:
                    pass

    # Función para dibujar el cartel de las tiendas y de la puerta final
    def dibujar_cartel(self, inventory, mensaje=None):
        self.cartel_active = True  
        self.opcion_seleccionada = 0
        if mensaje is None:
            mensaje = self.message

        self.update = 0
        self.longitud_actual = 0
        opciones_renderizadas = False

        while self.cartel_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if opciones_renderizadas:
                        if event.key == pygame.K_UP:
                            self.opcion_seleccionada = max(0, self.opcion_seleccionada - 1)
                        elif event.key == pygame.K_DOWN:
                            self.opcion_seleccionada = min(len(self.opciones) - 1, self.opcion_seleccionada + 1)

            dialogo_ancho = 850
            dialogo_alto = -100
            dialogo_x = SCREEN_WIDTH // 2 - dialogo_ancho // 2
            dialogo_y = SCREEN_HEIGHT // 2 - dialogo_alto // 2
            inicio_texto_x = dialogo_x + (dialogo_ancho - 350) // 2
            inicio_texto_y = dialogo_y + (dialogo_alto - 30) // 2 + 100

            self.pantalla.blit(self.imagen_cartel, (inicio_texto_x, inicio_texto_y))

            tiempo_actual = time.time()
            if tiempo_actual - self.update > 0.05:
                if self.longitud_actual < len(mensaje):
                    self.longitud_actual += 1
                    self.update = tiempo_actual

            texto_mostrado = mensaje[:self.longitud_actual]
            self.dibujar_frases(texto_mostrado, inicio_texto_x + 30, inicio_texto_y + 30, max_ancho_linea=350)

            if mensaje == self.message and self.longitud_actual == len(mensaje):
                self.opciones = ["Introducir Llave", "Esperar"]
                opciones_y = inicio_texto_y + 80 + (len(self.opciones) * 30) // 2
                for indice, opcion in enumerate(self.opciones):
                    color = (255, 0, 0) if indice == self.opcion_seleccionada else self.MARRON
                    opcion_texto = self.fuente.render(opcion, True, color)
                    self.pantalla.blit(opcion_texto, (inicio_texto_x + 30, opciones_y + indice * 30))
                opciones_renderizadas = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_x]:
                self.cartel_active = False
                if mensaje == self.message and opciones_renderizadas:
                    if self.opcion_seleccionada == 0 and inventory.get_llave():
                        self.sonido_llaves.play()
                        inventory.eliminar_llave()
                        self.cartel_procesado = True 
                        return True
                    elif self.opcion_seleccionada == 1:
                        self.cartel_procesado = True
                        return False
                else:
                    return False
            pygame.display.flip()

    # Función para dibujar letra a letra el diálogo
    def dibujar_frases(self, texto_mostrado, inicio_texto_x, inicio_texto_y, max_ancho_linea=450, color_texto=None):
        palabras = texto_mostrado.split(' ')
        linea_actual = ""
        y_offset = 0
        self.caracter_especial_dibujado = False

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
            if self.marcador in linea_actual:
              self.caracter_especial_dibujado = True