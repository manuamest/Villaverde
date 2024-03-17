import pygame
import sys
import time
from settings import *

class MenuBase:
    def __init__(self, screen, menu_options, background_image, background_rect):
        # Inicialización de la clase base del menú con los parámetros dados
        self.screen = screen
        self.menu_options = menu_options
        self.selected_option = 0  # Opción seleccionada por defecto
        self.background_image = background_image  # Imagen de fondo del menú
        self.background_rect = background_rect  # Rectángulo que define el área de la imagen de fondo
        # Fuente para el texto del menú
        self.font = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 40)
        # Carga de la imagen de los controles
        self.imagen_controles = pygame.image.load('./code/sprites/controles/controles.png').convert_alpha()
        # Escalado de la imagen de los controles
        self.imagen_controles_ampliada = pygame.transform.scale(self.imagen_controles, (800, 400))
        # Posición de los controles en la pantalla
        self.posicion_controles = (SCREEN_WIDTH//2-800//2, SCREEN_HEIGHT//2-400//2)
        self.should_return_flag = False  # Flag para indicar si se debe volver atrás
        # Texto para la opción de continuar
        self.continue_text = self.font.render('Continuar', True, (255, 255, 255))
        # Texto para la opción de salir del juego
        self.quit_text = self.font.render('Salir del juego', True, (255, 255, 255))
        # Rectángulos que definen la posición de los textos de continuar y salir del juego
        self.continue_text_rect = self.continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.quit_text_rect = self.quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    def show_pause_menu(self):
        # Método para mostrar el menú de pausa
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.imagen_controles_ampliada, self.posicion_controles)
        pygame.display.flip()

    def show_menu(self):
        # Método para mostrar el menú principal
        self.screen.blit(self.background_image, self.background_rect)
        for i, option in enumerate(self.menu_options):
            # Rectángulo que representa cada opción del menú
            bar_rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 100 + i * 60, SCREEN_WIDTH // 3, 40)
            pygame.draw.rect(self.screen, (168, 104, 47) if i == self.selected_option else (211, 132, 60), bar_rect, border_radius=10)
            pygame.draw.rect(self.screen, 'black', bar_rect, 2, border_radius=10)
            color = 'white'
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100 + i * 60 + 20))
            self.screen.blit(text, text_rect)
        
        # Agregar mensaje en la parte inferior
        bottom_font = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 20)  # Fuente más pequeña
        bottom_text = bottom_font.render("Utiliza las flechas del teclado para cambiar de opcion y 'Enter' para confirmar.", True, (255, 255, 255))
        bottom_text_rect = bottom_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))  # Posición ajustada
        
        # Renderizar el texto en negro con un ligero desplazamiento para crear el borde
        bottom_text_shadow = bottom_font.render("Utiliza las flechas del teclado para cambiar de opcion y 'Enter' para confirmar.", True, (0, 0, 0))
        bottom_text_shadow_rect = bottom_text_shadow.get_rect(center=(bottom_text_rect.centerx + 1, bottom_text_rect.centery + 1))
        
        # Mostrar el texto de sombra (borde)
        self.screen.blit(bottom_text_shadow, bottom_text_shadow_rect)
        
        # Mostrar el texto original (blanco)
        self.screen.blit(bottom_text, bottom_text_rect)

        pygame.display.flip()

    def handle_key_return(self):
        # Método para manejar la pulsación de la tecla de retorno
        pass

    def run(self):
        # Método para ejecutar el menú
        pass

    def get_should_return(self):
        # Método para obtener si se debe volver atrás
        return self.should_return_flag


class Menu(MenuBase):
    def __init__(self, screen, clock):
        # Inicialización de la clase Menu con la pantalla y el reloj
        menu_options = ["Jugar", "Opciones", "Controles", "Salir"]  # Opciones del menú
        # Carga de la imagen de fondo del menú
        self.background_image = pygame.image.load('./code/PantallaTitulo.png').convert()
        original_width, original_height = self.background_image.get_size()
        new_height = SCREEN_HEIGHT
        new_width = int((new_height / original_height) * original_width)
        self.background_image = pygame.transform.scale(self.background_image, (new_width, new_height))
        # Rectángulo que define el área de la imagen de fondo
        self.background_rect = self.background_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        super().__init__(screen, menu_options, self.background_image, self.background_rect)
        self.screen = screen
        self.clock = clock
        self.showing_controls = False  # Flag para indicar si se están mostrando los controles

    def show_start_screen(self):
        # Método para mostrar la pantalla de inicio
        waiting = True
        text_flash_timer = 0
        flash_interval = 150  # Intervalo de tiempo para el parpadeo del texto
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
            text_rect = font_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

            if show_text:
                for dx in [-2, 0, 2]:
                    for dy in [-2, 0, 2]:
                        self.screen.blit(font_surface, (text_rect.x + dx, text_rect.y + dy))

                font_surface = font.render(text, True, 'white')
                self.screen.blit(font_surface, text_rect)

            pygame.display.flip()

            self.clock.tick(FPS)
            
    def handle_key_return(self):
        # Método para manejar la pulsación de la tecla de retorno
        if self.selected_option == 0:  # Jugar
            self.in_menu = False
        elif self.selected_option == 1:  # Opciones
            self.options = Options(self.screen, self.clock, self.background_image, self.background_rect, self.tutorial_enabled, self.full_screen)
        elif self.selected_option == 2:  # Controles
            self.showing_controls = True
        elif self.selected_option == 3:  # Salir
            pygame.quit()
            sys.exit()

    def run(self):
        # Método para ejecutar el menú
        self.in_menu = True
        self.options = None
        self.tutorial_enabled = True
        self.full_screen = False
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
                self.full_screen = self.options.get_full_screen_enabled()
                if self.options.get_should_return():
                    self.options = None
            if self.showing_controls:
                self.screen.blit(self.imagen_controles_ampliada, self.posicion_controles)
                pygame.display.flip()
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.showing_controls = False
                        break
            else:
                self.show_menu()
            
            self.clock.tick(FPS)

class Options(MenuBase):
    def __init__(self, screen, clock, background_image, background_rect, tutorial_enabled, full_screen):
        # Inicialización de la clase Options con los parámetros dados
        self.screen = screen
        self.clock = clock
        self.background_image = background_image  # Imagen de fondo de las opciones
        self.background_rect = background_rect  # Rectángulo que define el área de la imagen de fondo
        self.tutorial_enabled = tutorial_enabled  # Estado del tutorial (activado/desactivado)
        menu_options = ["", "", "Volver"]  # Opciones del menú de opciones
        super().__init__(screen, menu_options, self.background_image, self.background_rect)
        self.full_screen = full_screen  # Estado de pantalla completa (activado/desactivado)

    def handle_key_return(self):
        # Método para manejar la pulsación de la tecla de retorno
        if self.selected_option == 0:  # Activar/Desactivar tutorial
            self.tutorial_enabled = not self.tutorial_enabled
        elif self.selected_option == 1:  # Cambiar a modo ventana/pantalla completa
            pygame.display.toggle_fullscreen()
            self.full_screen = not self.full_screen
        elif self.selected_option == 2:  # Volver
            self.in_options = False
            self.should_return_flag = True

    def show_menu(self):
        # Método para mostrar el menú de opciones
        super().show_menu()
        # Actualización de las opciones del menú según el estado actual
        self.menu_options[0] = "Desactivar Tutorial" if self.tutorial_enabled else "Activar Tutorial"
        self.menu_options[1] = "Ventana" if self.full_screen else "Pantalla Completa"

    def run(self):
        # Método para ejecutar el menú de opciones
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
        # Método para obtener si el tutorial está activado
        return self.tutorial_enabled

    def get_full_screen_enabled(self):
        # Método para obtener si el modo pantalla completa está activado
        return self.full_screen
