import pygame
import sys
import time
from settings import *

class MenuBase:
    def __init__(self, screen, menu_options, background_image, background_rect):
        self.screen = screen
        self.menu_options = menu_options
        self.selected_option = 0
        self.background_image = background_image
        self.background_rect = background_rect
        self.font = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 40)
        self.should_return_flag = False        
        self.continue_text = self.font.render('Continuar', True, (255, 255, 255))
        self.quit_text = self.font.render('Salir del juego', True, (255, 255, 255))
        self.continue_text_rect = self.continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.quit_text_rect = self.quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    def show_pause_menu(self):
        self.screen.blit(self.continue_text, self.continue_text_rect)
        self.screen.blit(self.quit_text, self.quit_text_rect)

    def show_menu(self):
        self.screen.blit(self.background_image, self.background_rect)
        for i, option in enumerate(self.menu_options):
            bar_rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 100 + i * 60, SCREEN_WIDTH // 3, 40)  # Ajusta el alto y el ancho aquí
            pygame.draw.rect(self.screen, (168, 104, 47) if i == self.selected_option else (211, 132, 60), bar_rect, border_radius=10)
            pygame.draw.rect(self.screen, 'black', bar_rect, 2, border_radius=10)
            color = 'white'
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100 + i * 60 + 20))  # Ajusta la posición vertical aquí
            self.screen.blit(text, text_rect)
        pygame.display.flip()


    def handle_key_return(self):
        pass

    def run(self):
        pass

    def get_should_return(self):
        return self.should_return_flag


class Menu(MenuBase):
    def __init__(self, screen, clock):
        menu_options = ["Jugar", "Opciones", "Controles", "Salir"]
        # Fondo
        self.background_image = pygame.image.load('./code/PantallaTitulo.png').convert()
        original_width, original_height = self.background_image.get_size()
        new_height = SCREEN_HEIGHT
        new_width = int((new_height / original_height) * original_width)
        self.background_image = pygame.transform.scale(self.background_image, (new_width, new_height))
        self.background_rect = self.background_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        super().__init__(screen, menu_options, self.background_image, self.background_rect)
        self.screen = screen
        self.clock = clock

    def show_start_screen(self):
        waiting = True
        text_flash_timer = 0
        flash_interval = 150  # Intervalo de parpadeo en milisegundos
        show_text = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

            # Dibujar la imagen de fondo centrada
            self.screen.blit(self.background_image, self.background_rect)

            # Mensaje en la pantalla de inicio (ajustado hacia abajo)
            font = pygame.font.Font(None, 36)
            text = "Presiona Enter para comenzar"

            # Actualizar el parpadeo del texto
            text_flash_timer += self.clock.get_rawtime()
            if text_flash_timer > flash_interval:
                show_text = not show_text
                text_flash_timer = 0

            # Renderizar texto con borde
            font_surface = font.render(text, True, 'black')
            text_rect = font_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

            # Dibujar texto con borde
            if show_text:
                for dx in [-2, 0, 2]:
                    for dy in [-2, 0, 2]:
                        self.screen.blit(font_surface, (text_rect.x + dx, text_rect.y + dy))

                # Renderizar texto real
                font_surface = font.render(text, True, 'white')
                self.screen.blit(font_surface, text_rect)

            pygame.display.flip()

            # Restablecer el temporizador para evitar una acumulación innecesaria
            self.clock.tick(FPS)
            
    def handle_key_return(self):
        if self.selected_option == 0:  # Jugar
            self.in_menu = False
        elif self.selected_option == 1:  # Opciones
            self.options = Options(self.screen, self.clock, self.background_image, self.background_rect)
            print("Mostrar Opciones")  # Agrega lógica de opciones aquí
        elif self.selected_option == 2:  # Controles
            print("Mostrar Controles")  # Agrega lógica de controles aquí
        elif self.selected_option == 3:  # Salir
            pygame.quit()
            sys.exit()

    def run(self):
        self.in_menu = True
        self.options = None
        self.tutorial_enabled = True

        while self.in_menu:
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
                        self.handle_key_return()

            if self.options:
                self.options.run()
                self.tutorial_enabled = self.options.get_tutorial_enabled()
                if self.options.get_should_return():
                    self.options = None

            self.show_menu()
            self.clock.tick(FPS)

class Options(MenuBase):
    def __init__(self, screen, clock, background_image, background_rect):
        self.screen = screen
        self.clock = clock
        self.background_image = background_image 
        self.background_rect = background_rect
        self.tutorial_enabled = True
        self.tutorial_option_text = "Desactivar Tutorial"
        self.fullscreen_option_text = "Pantalla Completa"
        menu_options = [self.tutorial_option_text, self.fullscreen_option_text, "Volver"]
        super().__init__(screen, menu_options, self.background_image, self.background_rect)

    def handle_key_return(self):
        if self.selected_option == 0:  # Activar o Desactivar Tutorial
            self.tutorial_enabled = not self.tutorial_enabled
            self.tutorial_option_text = "Desactivar Tutorial" if self.tutorial_enabled else "Activar Tutorial"
            print(f'El tutorial está a: {self.tutorial_enabled}')
        elif self.selected_option == 1:  # Pantalla Completa
            pygame.display.toggle_fullscreen()
            self.fullscreen_option_text = "Ventana" if self.fullscreen_option_text == 'Pantalla Completa' else "Pantalla Completa"
        elif self.selected_option == 2:  # Volver
            self.in_options = False
            self.should_return_flag = True

    def show_menu(self):
        super().show_menu()
        self.menu_options[0] = self.tutorial_option_text
        self.menu_options[1] = self.fullscreen_option_text


    def run(self):
        self.in_options = True

        while self.in_options:
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
                        self.handle_key_return()

            self.show_menu()
            self.clock.tick(FPS)

    def get_tutorial_enabled(self):
        return self.tutorial_enabled