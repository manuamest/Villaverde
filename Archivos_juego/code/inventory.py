import pygame
from settings import *
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Inventory:
    def __init__(self,screen):
        # Cargar fuentes
        self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 24)
        self.pantalla = screen
        self.pantalla_ancho = SCREEN_WIDTH
        self.pantalla_alto = SCREEN_HEIGHT
        self.screen = screen
        # Colores
        self.COLOR_LETRAS = (238, 212, 167)
        self.MARRON = (177, 75, 1)
        self.GRIS = (200, 200, 200)
        # Variables del inventario
        self.inventario_abierto = False
        self.inventario_items = {"Madera": 0, "Trigo": 0,"Bolsa de dinero":0,"Jordan":0,"Bufanda y boina":0,"Gafas y cadena":0,"Llave magistral":0}

        self.imagen_fondo_inventario = pygame.image.load('./code/sprites/inventarios/verano.png').convert_alpha()
        self.imagen_fondo_inventario = pygame.transform.scale(self.imagen_fondo_inventario, (400, 300))
        self.imagen_fondo_inventario.set_alpha(200)

        self.sprites_items = {
            "Madera": pygame.image.load('./code/sprites/madera.png'),
            "Trigo": pygame.image.load('./code/sprites/trigo.png'),
            "Bolsa de dinero": pygame.image.load('./code/sprites/dinero.png'),
            "Bufanda y boina": pygame.image.load('./code/sprites/bufanda_y_boina.png'),
            "Jordan": pygame.image.load('./code/sprites/jordan.png'),
            "Gafas y cadena": pygame.image.load('./code/sprites/gafas.png'),
            "Llave magistral": pygame.image.load('./code/sprites/llavemagistral.png')
        }

    def cambiar_imagen_inventario(self, estacion):
        if estacion == "otoño":
            nueva_imagen = pygame.image.load('./code/sprites/inventarios/otoño.png').convert_alpha()
        else:
            nueva_imagen = pygame.image.load('./code/sprites/inventarios/invierno.png').convert_alpha()
        nueva_imagen = pygame.transform.scale(nueva_imagen, (400, 300))
        nueva_imagen.set_alpha(200)
        # Actualizar la imagen de fondo del inventario
        self.imagen_fondo_inventario = nueva_imagen

    def añadir_madera(self):
        self.inventario_items["Madera"] += 5

    def eliminar_madera(self,cantidad):
        self.inventario_items["Madera"] -= cantidad
    
    def eliminar_trigo(self,cantidad):
        self.inventario_items["Trigo"] -= cantidad

    def añadir_dinero_mercader(self,cantidad):
        self.inventario_items["Bolsa de dinero"] += cantidad

    def añadir_trigo(self):
        self.inventario_items["Trigo"] += 1

    def añadir_dinero(self):
        self.inventario_items["Bolsa de dinero"] += 100

    def añadir_jordan(self):
        self.inventario_items["Jordan"] += 1
    
    def añadir_bufandas(self):
        self.inventario_items["Bufanda y boina"] += 1
    
    def añadir_llave(self):
        self.inventario_items["Llave magistral"] += 1
    
    def añadir_gafas(self):
        self.inventario_items["Gafas y cadena"] += 1
    
    def eliminar_llave(self):
        self.inventario_items["Llave magistral"] -= 1
       
    def eliminar_gafas(self):
        self.inventario_items["Gafas y cadena"] -= 1
    
    def eliminar_jordan(self):
        self.inventario_items["Jordan"] -= 1

    def eliminar_bufandas(self):
        self.inventario_items["Bufanda y boina"] -= 1

    def eliminar_dinero(self,cantidad):
        self.inventario_items["Bolsa de dinero"] -= cantidad

    def eliminar_dinero_modista(self,cantidad):
        self.inventario_items["Bolsa de dinero"] -= cantidad

    def get_dinero(self):
        return self.inventario_items["Bolsa de dinero"] 
    
    def get_trigo(self):
        return self.inventario_items["Trigo"] 
    
    def get_madera(self):
        return self.inventario_items["Madera"]
     
    def get_bufandas(self):
        return self.inventario_items["Bufanda y boina"]
    
    def get_gafas(self):
        return self.inventario_items["Gafas y cadena"]
    
    def get_jordan(self):
        return self.inventario_items["Jordan"]
    
    def get_llave(self):
        return self.inventario_items["Llave magistral"]

    # Función para dibujar el inventario
    def dibujar_inventario(self, inventario_x=None, inventario_y=None, not_transparencia=False):
        inventario_ancho = 400
        inventario_alto = 300
        if inventario_x is None:
            inventario_x = self.pantalla_ancho // 2 - inventario_ancho // 2
        if inventario_y is None:
            inventario_y = self.pantalla_alto // 2 - inventario_alto // 2
        if not_transparencia:
            self.imagen_fondo_inventario.set_alpha(255)
        self.pantalla.blit(self.imagen_fondo_inventario, (inventario_x, inventario_y))

        barra_alto_interior = 36
        ajuste_y = 0
        barra_ancho = 200  # Nuevo ancho de la barra

        for i, (item, cantidad) in enumerate(self.inventario_items.items()):
            if cantidad > 0:
                texto = self.fuente.render(f"{item}: {cantidad}", True, self.COLOR_LETRAS)
                barra_x = inventario_x + 20 + 29
                barra_y = inventario_y + 20 + (i * 50) + 29 - ajuste_y
                pygame.draw.rect(self.pantalla, (0, 0, 0), (barra_x, barra_y, barra_ancho, 40), border_radius=5)
                pygame.draw.rect(self.pantalla, self.MARRON, (barra_x + 2, barra_y + 2, barra_ancho - 4, 36), border_radius=5)
                texto_x = barra_x + 10
                texto_y = barra_y + (40 - texto.get_height()) // 2
                self.pantalla.blit(texto, (texto_x, texto_y))
                sprite = self.sprites_items[item]
                sprite_escalado = pygame.transform.scale(sprite, (int(sprite.get_width() * barra_alto_interior / sprite.get_height()), barra_alto_interior))
                sprite_x = barra_x - sprite_escalado.get_width() - 2  # Ajustar posición del sprite
                self.pantalla.blit(sprite_escalado, (sprite_x, barra_y + 2))
            else:
                ajuste_y += 50
