import pygame
import sys
from game import Game
from menu import Menu

class Director:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Villaverde')
        self.clock = pygame.time.Clock()

        self.game = Game()
        self.menu = Menu(self.screen, self.clock, self.game.level, self.game.soil_layer, self.game.last_growth_time)

    def run(self):
        self.menu.show_start_screen()
        self.menu.run()

        # Cuando se sale del menú, comenzamos el juego
        self.game.run()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Si se presiona la tecla Escape, pausar o reanudar el juego
                    self.game.toggle_pause()

    def update(self):
        self.handle_events()
        self.game.update()

    def draw(self):
        self.game.draw()
        pygame.display.flip()

    def main_loop(self):
        while True:
            self.update()
            self.draw()
            self.clock.tick(FPS)
