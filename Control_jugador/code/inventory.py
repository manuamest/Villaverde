import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana
pantalla_ancho = 800
pantalla_alto = 600
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))

# Cargar fuentes
try:
    fuente = pygame.font.Font("Arial.ttf", 24)  # Intenta cargar una fuente personalizada
except FileNotFoundError:
    fuente = pygame.font.SysFont("Arial", 24)  # Si no se encuentra, usa una fuente del sistema

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
AZUL_CLARO = (173, 216, 230)

# Variables del inventario
inventario_abierto = False
# Cambiado a un diccionario con ítems y sus cantidades
inventario_items = {"Madera": 5, "Trigo": 3}

# Función para dibujar el inventario
def dibujar_inventario():
    # Dimensiones del inventario
    inventario_ancho = 400
    inventario_alto = 300
    inventario_x = pantalla_ancho // 2 - inventario_ancho // 2
    inventario_y = pantalla_alto // 2 - inventario_alto // 2

    # Dibujar el fondo del inventario
    fondo = pygame.Surface((inventario_ancho, inventario_alto))
    fondo.fill(AZUL_CLARO)
    fondo.set_alpha(230)  # Semi transparencia
    pantalla.blit(fondo, (inventario_x, inventario_y))
    pygame.draw.rect(pantalla, NEGRO, (inventario_x, inventario_y, inventario_ancho, inventario_alto), 3)  # Borde

    # Dibujar los items del inventario y sus cantidades
    for i, (item, cantidad) in enumerate(inventario_items.items()):
        texto = fuente.render(f"{item}: {cantidad}", True, NEGRO)
        item_x = inventario_x + 20
        item_y = inventario_y + 20 + i * 50  # Espaciado aumentado para mejor visualización
        pygame.draw.rect(pantalla, BLANCO, (item_x - 10, item_y - 10, 360, 40), 0, 5)  # Fondo de ítem
        pantalla.blit(texto, (item_x, item_y))

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_b:
                inventario_abierto = not inventario_abierto

    # Rellenar el fondo
    pantalla.fill(GRIS)

    # Dibujar el inventario si está abierto
    if inventario_abierto:
        dibujar_inventario()

    # Actualizar la pantalla
    pygame.display.flip()
