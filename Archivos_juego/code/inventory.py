import pygame
from settings import *

class Inventory:
    def __init__(self, screen):
        self.pantalla = screen

        # Cargar fuentes
        self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 24)

        # Colores
        self.COLOR_LETRAS = (238, 212, 167)
        self.MARRON = (128, 58, 58)
        self.GRIS = (200, 200, 200)

        # Variables del inventario
        self.inventario_abierto = False
        self.inventario_items = {   "Madera": 0, 
                                    "Trigo": 0,
                                    "Bolsa de dinero":0,
                                    "Zapatillas":0,
                                    "Bufandas":0}

        # Cargar la imagen de fondo para el inventario y hacerla semi-transparente
        self.imagen_fondo_inventario = pygame.image.load('./code/sprites/inventario.png').convert_alpha()
        self.imagen_fondo_inventario = pygame.transform.scale(self.imagen_fondo_inventario, (400, 300))
        self.imagen_fondo_inventario.set_alpha(200)

        self.sprites_items = {
            "Madera": pygame.image.load('./code/sprites/madera.png'),
            "Trigo": pygame.image.load('./code/sprites/trigo.png'),
            "Bolsa de dinero": pygame.image.load('./code/sprites/dinero.png'),
            'Bufandas': pygame.image.load('./code/sprites/bufanda_y_boina.png'),
            'Zapatillas': pygame.image.load('./code/sprites/jordan.png'),
        }

    def añadir_madera(self):
        self.inventario_items["Madera"] += 1

    def eliminar_madera(self,cantidad):
        self.inventario_items["Madera"] -= cantidad
    
    def eliminar_trigo(self,cantidad):
        self.inventario_items["Trigo"] -= cantidad

    def añadir_dinero_mercader(self,cantidad):
        self.inventario_items["Bolsa de dinero"] += cantidad

    def añadir_trigo(self):
        self.inventario_items["Trigo"] += 1

    def añadir_dinero(self):
        self.inventario_items["Bolsa de dinero"] += 1

    def añadir_zapatillas(self):
        self.inventario_items["Zapatillas"] += 1
    
    def añadir_bufandas(self):
        self.inventario_items["Bufandas"] += 1

  

    def eliminar_dinero(self):
        self.inventario_items["Bolsa de dinero"] -= 1

    def eliminar_dinero_modista(self,cantidad):
        self.inventario_items["Bolsa de dinero"] -= cantidad

    def get_dinero(self):
        return self.inventario_items["Bolsa de dinero"] 
    
    def get_trigo(self):
        return self.inventario_items["Trigo"] 
    
    def get_madera(self):
        return self.inventario_items["Madera"]

    def get_zapatillas(self):
        return self.inventario_items["Zapatillas"]
    
    def is_empty(self):
        return sum(self.inventario_items.values()) == 0
    

    # Función para dibujar el inventario
    def dibujar_inventario(self):
        inventario_ancho = 400
        inventario_alto = 300
        inventario_x = SCREEN_WIDTH // 2 - inventario_ancho // 2
        inventario_y = SCREEN_HEIGHT // 2 - inventario_alto // 2

        # Dibujar la imagen de fondo para el inventario
        self.pantalla.blit(self.imagen_fondo_inventario, (inventario_x, inventario_y))

        barra_alto_interior = 36  # Altura interior de la barra para ajustar el sprite

        # Variable para ajustar la posición y de las barras cuando alguna cantidad es 0
        ajuste_y = 0

        for i, (item, cantidad) in enumerate(self.inventario_items.items()):
            if cantidad > 0:  # Solo dibujar si la cantidad del ítem es mayor que 0
                texto = self.fuente.render(f"{item}: {cantidad}", True, self.COLOR_LETRAS)
                barra_x = inventario_x + 20 + 29
                barra_y = inventario_y + 20 + (i * 50) + 29 - ajuste_y

                # Dibujar el borde negro y la barra marrón
                pygame.draw.rect(self.pantalla, (0, 0, 0), (barra_x, barra_y, 300, 40), border_radius=5)
                pygame.draw.rect(self.pantalla, self.MARRON, (barra_x + 2, barra_y + 2, 296, 36), border_radius=5)

                # Dibujar el texto
                texto_x = barra_x + 10
                texto_y = barra_y + (40 - texto.get_height()) // 2
                self.pantalla.blit(texto, (texto_x, texto_y))

                # Ajustar y dibujar el sprite
                sprite = self.sprites_items[item]  # Obtén el sprite para el ítem actual
                sprite_escalado = pygame.transform.scale(sprite, (int(sprite.get_width() * barra_alto_interior / sprite.get_height()), barra_alto_interior))
                sprite_x = barra_x + 300 - sprite_escalado.get_width() - 2
                self.pantalla.blit(sprite_escalado, (sprite_x, barra_y + 2))
            else:
                # Ajustar la posición y de las siguientes barras si la cantidad actual es 0
                ajuste_y += 50
