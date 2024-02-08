import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana
pantalla_ancho = 800
pantalla_alto = 600
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))

# Cargar fuentes

fuente = pygame.font.Font("./fonts/Stardew_Valley.ttf", 24)

# Colores
COLOR_LETRAS = (238, 212, 167)
MARRON = (128, 58, 58)
GRIS = (200, 200, 200)

# Variables del inventario
inventario_abierto = False
inventario_items = {"Madera": 0, "Trigo": 0}

def añadir_madera():
    global inventario_items
    inventario_items["Madera"] += 1

def añadir_trigo():
    global inventario_items
    inventario_items["Trigo"] += 1


# Cargar la imagen de fondo para el inventario
# Asegúrate de que la imagen 'inventario_fondo.png' está en el mismo directorio que tu script
imagen_fondo_inventario = pygame.image.load('./sprites/inventario.png')
imagen_fondo_inventario = pygame.transform.scale(imagen_fondo_inventario, (400, 300))




sprites_items = {
    "Madera": pygame.image.load('./sprites/madera.png'),
    "Trigo": pygame.image.load('./sprites/trigo.png'),

}

# Función para dibujar el inventario
def dibujar_inventario():
    inventario_ancho = 400
    inventario_alto = 300
    inventario_x = pantalla_ancho // 2 - inventario_ancho // 2
    inventario_y = pantalla_alto // 2 - inventario_alto // 2

    # Dibujar la imagen de fondo para el inventario
    pantalla.blit(imagen_fondo_inventario, (inventario_x, inventario_y))

    barra_alto_interior = 36  # Altura interior de la barra para ajustar el sprite

    # Variable para ajustar la posición y de las barras cuando alguna cantidad es 0
    ajuste_y = 0

    for i, (item, cantidad) in enumerate(inventario_items.items()):
        if cantidad > 0:  # Solo dibujar si la cantidad del ítem es mayor que 0
            texto = fuente.render(f"{item}: {cantidad}", True, COLOR_LETRAS)
            barra_x = inventario_x + 20 + 29
            barra_y = inventario_y + 20 + (i * 50) + 29 - ajuste_y

            # Dibujar el borde negro y la barra marrón
            pygame.draw.rect(pantalla, (0, 0, 0), (barra_x, barra_y, 300, 40), border_radius=5)
            pygame.draw.rect(pantalla, MARRON, (barra_x + 2, barra_y + 2, 296, 36), border_radius=5)

            # Dibujar el texto
            texto_x = barra_x + 10
            texto_y = barra_y + (40 - texto.get_height()) // 2
            pantalla.blit(texto, (texto_x, texto_y))

            # Ajustar y dibujar el sprite
            sprite = sprites_items[item]  # Obtén el sprite para el ítem actual
            sprite_escalado = pygame.transform.scale(sprite, (int(sprite.get_width() * barra_alto_interior / sprite.get_height()), barra_alto_interior))
            sprite_x = barra_x + 300 - sprite_escalado.get_width() - 2
            pantalla.blit(sprite_escalado, (sprite_x, barra_y + 2))
        else:
            # Ajustar la posición y de las siguientes barras si la cantidad actual es 0
            ajuste_y += 50

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_b:
                inventario_abierto = not inventario_abierto
            elif evento.key == pygame.K_m:  # Al presionar M, añade madera
                añadir_madera()
            elif evento.key == pygame.K_t:  # Al presionar T, añade trigo
                añadir_trigo()

    # Rellenar el fondo
    pantalla.fill(GRIS)

    # Dibujar el inventario si está abierto
    if inventario_abierto:
        dibujar_inventario()

    # Actualizar la pantalla
    pygame.display.flip()
