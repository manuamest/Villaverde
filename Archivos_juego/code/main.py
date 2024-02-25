import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        icon_path = "./code/sprites/icono.png"
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Villaverde')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.menu_options = ["Jugar", "Opciones", "Controles", "Salir"]
        self.selected_option = 0

        # Cargar la imagen de fondo
        self.background_image = pygame.image.load('./code/villaverde.jpg').convert()
        original_width, original_height = self.background_image.get_size()
        new_height = SCREEN_HEIGHT
        new_width = int((new_height / original_height) * original_width)
        self.background_image = pygame.transform.scale(self.background_image, (new_width, new_height))

        # Obtener la posición centrada para la imagen
        self.background_rect = self.background_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

	    # Cargar música de fondo
        pygame.mixer.music.load('./code/villaverde.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Repetir infinitamente

    def show_start_screen(self):
        waiting = True
        text_flash_timer = 0
        flash_interval = 200  # Intervalo de parpadeo en milisegundos
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
            text_rect = font_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 220))

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



    def show_menu(self):
        # Dibujar la imagen de fondo centrada
        self.screen.blit(self.background_image, self.background_rect)

        # Dibujar barras estrechas con forma redondeada en las esquinas detrás de las opciones del menú
        font = pygame.font.Font(None, 36)
        for i, option in enumerate(self.menu_options):
            bar_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + i * 50, SCREEN_WIDTH // 2, 30)
            pygame.draw.rect(self.screen, (168, 82, 52), bar_rect, border_radius=10)
            pygame.draw.rect(self.screen, 'black', bar_rect, 2, border_radius=10)

            color = 'white' if i == self.selected_option else (100, 100, 100)
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50 + 15))
            self.screen.blit(text, text_rect)

        pygame.display.flip()


    def run(self):
        self.show_start_screen()  # Mostrar pantalla de inicio

        in_menu = True
        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % (len(self.menu_options) + 1)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % (len(self.menu_options) + 1)
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

        # Salir del menú y entrar al bucle principal del juego
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(FPS) / 700
            self.level.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
