import pygame
import random
import time
from sprites import *
from settings import *

class Puzle:
    def __init__(self):
        self.puzle_ancho, self.puzle_alto = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Ajustar según necesidad
        self.puzle_surface = pygame.Surface((self.puzle_ancho, self.puzle_alto))
        self.puzle_surface.set_alpha(200)
        self.puzle_x = (SCREEN_WIDTH - self.puzle_ancho) // 2
        self.puzle_y = (SCREEN_HEIGHT - self.puzle_alto) // 2

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.puzle_activo = False
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False
        self.playing = False
        self.complete = False
        self.grid_offset_x = 70 
        self.grid_offset_y = 70  
        self.imagen_fondo = pygame.image.load('./code/sprites/marco_puz.png')
        self.imagen_fondo_puzle = pygame.transform.scale(self.imagen_fondo, (640, 360)).convert_alpha()

    def create_game(self):
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0
        return grid   
    
    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        
        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]
            

    def draw_tiles(self):
        self.tiles = []
        for row, tiles_row in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile_num in enumerate(tiles_row):
                adjusted_x = col + self.grid_offset_x / TILESIZE
                adjusted_y = row + self.grid_offset_y / TILESIZE
                if tile_num != 0:
                    self.tiles[row].append(Tile(self, adjusted_x, adjusted_y, str(tile_num)))
                else:
                    self.tiles[row].append(Tile(self, adjusted_x, adjusted_y, "empty"))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(Button(350, 150, 200, 50, "INICIAR", WHITE, BLACK))
        self.draw_tiles()


    def run(self):
        self.playing = True
        if self.complete:
            return
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                self.complete = True 
                self.playing = False

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    def draw_grid(self):
         # Dibujar líneas verticales del grid
        for x in range(0, GAME_SIZE * TILESIZE + 1, TILESIZE): 
            pygame.draw.line(self.puzle_surface, LIGHTGREY, (x + self.grid_offset_x, 0 + self.grid_offset_y), (x + self.grid_offset_x, GAME_SIZE * TILESIZE + self.grid_offset_y))
        # Dibujar líneas horizontales del grid
        for y in range(0, GAME_SIZE * TILESIZE + 1, TILESIZE):  
            pygame.draw.line(self.puzle_surface, LIGHTGREY, (0 + self.grid_offset_x, y + self.grid_offset_y), (GAME_SIZE * TILESIZE + self.grid_offset_x, y + self.grid_offset_y))

    def draw(self):
        self.puzle_surface.blit(self.imagen_fondo_puzle, (0, 0))
        self.all_sprites.draw(self.puzle_surface)
        self.draw_grid()  

        for button in self.buttons_list:
            button.draw(self.puzle_surface)

        self.screen.blit(self.puzle_surface, (self.puzle_x, self.puzle_y))
        pygame.display.flip()


    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x = mouse_x - self.puzle_x
                mouse_y = mouse_y - self.puzle_y
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "INICIAR":
                            self.shuffle_time = 0
                            self.start_shuffle = True

    def start_puzle(self):
        self.new()  # Iniciar un nuevo juego
        self.run()  # Iniciar el bucle principal del juego