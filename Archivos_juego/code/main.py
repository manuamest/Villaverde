import pygame
import sys
import time
from settings import *
from level import Level, CameraGroup
from soil import SoilLayer
from menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        icon_path = "./code/sprites/icono.png"
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Villaverde')
        self.clock = pygame.time.Clock()
        self.all_sprites = CameraGroup()
        self.soil_layer = SoilLayer(self.all_sprites)
        self.last_growth_time = time.time()  # Tiempo de la última fase de crecimiento
        self.level = Level(self.soil_layer, self.all_sprites)

    def run(self, menu):
        menu.show_start_screen()
        menu.run()

if __name__ == '__main__':
    game = Game()
    menu = Menu(game.screen, game.clock, game.level, game.soil_layer, game.last_growth_time)
    game.run(menu=menu)

