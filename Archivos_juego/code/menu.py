import pygame
import sys
import time
from settings import *

class Menu:
    def __init__(self, screen, clock, level, soil_layer, last_growth_time=None):
        self.screen = screen
        self.clock = clock
        self.level = level
        self.soil_layer = soil_layer
        self.menu_options = ["Jugar", "Opciones", "Controles", "Salir"]
        self.selected_option = 0
        self.background_image = pygame.image.load('./code/villaverde.jpg').convert()
        original_width, original_height = self.background_image.get_size()
        new_height = SCREEN_HEIGHT
        new_width = int((new_height / original_height) * original_width)
        self.background_image = pygame.transform.scale(self.background_image, (new_width, new_height))
        self.background_rect = self.background_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.menu_font = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)
        self.last_growth_time = last_growth_time

    def show_menu(self):
        self.screen.blit(self.background_image, self.background_rect)
        for i, option in enumerate(self.menu_options):
            bar_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + i * 50, SCREEN_WIDTH // 2, 30)
            pygame.draw.rect(self.screen, (168, 82, 52), bar_rect, border_radius=10)
            pygame.draw.rect(self.screen, 'black', bar_rect, 2, border_radius=10)
            color = 'white' if i == self.selected_option else (100, 100, 100)
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50 + 15))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def show_start_screen(self):
        waiting = True
        text_flash_timer = 0
        flash_interval = 200
        show_text = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

            self.screen.blit(self.background_image, self.background_rect)
            font = pygame.font.Font(None, 36)
            text = "Presiona Enter para comenzar"
            text_flash_timer += self.clock.get_rawtime()
            if text_flash_timer > flash_interval:
                show_text = not show_text
                text_flash_timer = 0

            font_surface = font.render(text, True, 'black')
            text_rect = font_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 220))

            if show_text:
                for dx in [-2, 0, 2]:
                    for dy in [-2, 0, 2]:
                        self.screen.blit(font_surface, (text_rect.x + dx, text_rect.y + dy))
                font_surface = font.render(text, True, 'white')
                self.screen.blit(font_surface, text_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        in_menu = True
        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Jugar
                            in_menu = False
                        elif self.selected_option == 1:  # Opciones
                            print("Mostrar Opciones")  # Agrega lógica de opciones aquí
                        elif self.selected_option == 2:  # Controles
                            print("Mostrar Controles")  # Agrega lógica de controles aquí
                        elif self.selected_option == 3:  # Salir
                            pygame.quit()
                            sys.exit()
            self.show_menu()
            self.clock.tick(FPS)
                
                
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            current_time = time.time()
            elapsed_time = current_time - self.last_growth_time

            if elapsed_time >= 5:
                self.soil_layer.update_plants() 
                self.last_growth_time = current_time  

            dt = self.clock.tick(FPS) / 700
            self.level.run(dt)
            pygame.display.update()
