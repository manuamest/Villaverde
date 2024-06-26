from pygame.math import Vector2
# Pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64
FPS = 60

# Posiciones overlay 
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15), 
	'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10,
	'npc': 11
}

GROW_SPEED = {
	'trigo': 1,
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}

PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}

# Puzle
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
# Configuración del juego
WIDTH = 800
HEIGHT = 641
FPS = 60
title = "Resuelve el puzle para acceder a la mazmorra"
TILESIZE = 72
GAME_SIZE = 3