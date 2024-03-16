import pygame
from draw import Draw
from npcs_strategy import *
from animals_strategy import *

class Dialogue:
    def __init__(self,screen,escene,inventory):
            
            self.pantalla = screen
            self.escene = escene

            pygame.mixer.init()
            self.draw = Draw(screen,self,self.escene)
            self.draw.definir_dialogos()
        

            # Atributos
            self.opcion_escogida = False
            self.opcion_escogida_vaca = False
            self.opcion_escogida_pollo = False
            self.opcion_escogida_oveja = False
            self.opcion_seleccionada = 0
            self.dialogo_abierto = False
            self.material_dado = False
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
            self.opcion_escogida_obrero = False
            self.objetos_dados_a_jordi = False


            # Estrategia de cada personaje

            self.estrategias_dialogo = {
                "don diego": DialogoDonDiegoEstrategia(self.draw,self.escene),
                "obrero": DialogoObreroEstrategia(self.draw,self.escene),
                "hermanos": DialogoHermanosEstrategia(self.draw,self.escene),
                "mercader": DialogoMercaderEstrategia(self.draw,self.escene),
                "modista": DialogoModistaEstrategia(self.draw,self.escene),
                "pollo": DialogoPolloEstrategia(self.draw,self.escene),
                "vaca": DialogoVacaEstrategia(self.draw,self.escene),
                "oveja": DialogoOvejaEstrategia(self.draw,self.escene),
                "cabra": DialogoCabraEstrategia(self.draw,self.escene),
            }
        
            # Cantidades de materiales y accesorios
            self.cantidades = {
                "Madera": 0,
                "Trigo": 0,
                "Jordan": 0,
                "Bufanda y boina": 0,
                "Gafas y cadena":0
            }

           # Indices de cada personaje
            self.indices = {
                "don diego": 0,
                "obrero": 0,
                "mercader": 0,
                "modista": 0,
                "oveja":0,
                "pollo":0,
                "cabra":0,
                "vaca":0
            }


    # Setters 

    def set_indice_personaje(self, personaje, indice):
        self.indices[personaje] = indice
    
    def set_final_dialogo(self, final_dialogo):
        self.final_dialogo = final_dialogo
    
    def set_opcion_dialogo(self, dialogo_abierto):
        self.dialogo_abierto = dialogo_abierto
    
    def set_opcion_seleccionada(self, opcion):
        self.opcion_seleccionada = opcion
    
    def set_confirmacion_abierta(self, confirmacion_abierta):
        self.confirmacion_abierta = confirmacion_abierta
    
    def set_opcion_escogida(self, opcion_escogida):
        self.opcion_escogida = opcion_escogida
    
    def set_madera_dada(self, madera_dada):
        self.madera_dada = madera_dada
    
    def set_material_dado(self, material_dado):
        self.material_dado = material_dado
    
    def set_dinero_dado(self, dinero_dado):
        self.dinero_dado = dinero_dado
       
    def set_opcion_escogida_obrero(self, opcion_escogida_obrero):
        self.opcion_escogida_obrero = opcion_escogida_obrero
    
    def set_opcion_escogida_pollo(self, opcion_escogida_pollo):
        self.opcion_escogida_pollo = opcion_escogida_pollo

    def set_opcion_escogida_oveja(self, opcion_escogida_oveja):
        self.opcion_escogida_oveja = opcion_escogida_oveja
    
    def set_opcion_escogida_vaca(self, opcion_escogida_vaca):
        self.opcion_escogida_vaca = opcion_escogida_vaca
 
    def set_gafas_dadas(self, gafas_dadas):
        self.gafas_dadas = gafas_dadas
    
    def set_jordan_dadas(self, jordan_dadas):
        self.jordan_dadas = jordan_dadas
    
    def set_bufandas_dadas(self, bufandas_dadas):
        self.bufandas_dadas = bufandas_dadas
    
    def set_incr_llave(self,contador):
        self.contador_llave += contador
    
    def set_objetos_a_jordi(self, opcion):
        self.objetos_dados_a_jordi = opcion

        

    # Getters

    def obtener_indice_personaje(self, personaje):
        return self.indices.get(personaje, 0)

    def obtener_opcion_escogida(self):
        return self.opcion_escogida

  
    def obtener_madera_dada(self):
        return self.madera_dada
    

    def obtener_opcion_escogida_obrero(self):
        return self.opcion_escogida_obrero
    

    def obtener_opcion_escogida_pollo(self):
        return self.opcion_escogida_pollo
    

    def obtener_opcion_escogida_oveja(self):
        return self.opcion_escogida_oveja


    def obtener_opcion_escogida_vaca(self):
        return self.opcion_escogida_vaca


    def obtener_final_dialogo(self):
        return self.final_dialogo
    

    def get_gafas_dadas(self):
        return self.gafas_dadas
    

    def get_jordan_dadas(self):
        return self.jordan_dadas
    

    def get_bufandas_dadas(self):
        return self.bufandas_dadas


    def obtener_dialogo(self):
        return self.dialogo_abierto


    def obtener_material_dado(self):
        return self.material_dado


    def obtener_dinero_dado(self):
        return self.dinero_dado


    def obtener_confirmacion_abierta(self):
        return self.confirmacion_abierta

    def obtener_opcion_seleccionada(self):
        return self.opcion_seleccionada
    
    def get_contador_llave(self):
        return self.contador_llave
    
    def get_objetos_a_jordi(self):
        return self.objetos_dados_a_jordi
    

    # Función para calcular cuanto ofrece/cobra el mercader o la modista

    def calcular_pago(self, servicio, item, cantidad):
        precio = self.draw.precios.get(servicio, {}).get(item, 0)
        return precio * cantidad
    

    # Función para determinar qué dialogo hay que procesar

    def obtener_dialogo_personaje(self, personaje):
        estrategia = self.estrategias_dialogo.get(personaje)
        if estrategia:
            return estrategia.obtener_dialogo(self,self.escene,self.draw)
        else:
            return []
        
    # Función para la selección de las opiones de los personajes
        
    def manejar_opciones_personaje(self, keys, inventory, inicio_texto_x, inicio_texto_y, personaje):
        estrategia = self.estrategias_dialogo.get(personaje)
        if estrategia:
            opciones = estrategia.manejar_opciones(self,self.draw)

            if self.opcion_seleccionada is None:
                self.opcion_seleccionada = 0

            for indice, opcion in enumerate(opciones):
                color = (255, 0, 0) if indice == self.opcion_seleccionada else self.draw.MARRON
                opcion_texto = self.draw.fuente.render(opcion, True, color)
                self.pantalla.blit(opcion_texto, (inicio_texto_x, inicio_texto_y + 110 + indice * 30))
                
            if keys[pygame.K_UP] and self.opcion_seleccionada > 0:
                self.opcion_seleccionada -= 1
                self.draw.sonido_select.play()
            if keys[pygame.K_DOWN] and self.opcion_seleccionada < len(opciones) - 1:
                self.opcion_seleccionada += 1
                self.draw.sonido_select.play()

            if keys[pygame.K_x]:
                    estrategia.ejecutar_accion(inventory,self, personaje,self.draw)
                        
        else:
            print("No hay estrategia definida para este personaje.")

    
    # Función para determinar cuando se ha terminado un diálogo

    def manejar_interacciones(self, personaje, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual):
        estrategia = self.estrategias_dialogo.get(personaje)
    
        if estrategia:
            estrategia.manejar_interacciones(keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje,self,self.escene,self.draw)
        else:
            print("No hay estrategia definida para este personaje.")

    
