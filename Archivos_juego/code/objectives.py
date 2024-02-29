import pygame
from settings import *

class Objectives:
    def is_key_pressed(state, key):
        keys = pygame.key.get_pressed()
        if state:
            return True
        elif keys[key]:
            return True
        else:
            return False
        
    def inventory_is_not_empty(inventory):
        return not inventory.is_empty()
    
    def interact_with_npc(dialogue):
        return dialogue.obtener_dialogo() == True
    
    def last_step_tutorial(tutorial):
        return (tutorial.indice_tutorial) == (len(tutorial.tutorial_mensajes) - 1)
            
    def __init__(self, tutorial, inventory, dialogue):
        self.objectives = [
            Objective([
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_a), "1"),
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_w), "2"),
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_s), "3"),
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_d), "4")
            ], (lambda : tutorial.enable_next_step())),
            Objective([
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_q), "5"),
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_SPACE), "6"),
            ], (lambda : tutorial.enable_next_step())),
            Objective([
                Requirement(lambda state: Objectives.inventory_is_not_empty(inventory), "7")
            ], (lambda : tutorial.enable_next_step())),
            Objective([
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_b), "8")
            ], (lambda : tutorial.enable_next_step())),
            Objective([
                Requirement(lambda state: Objectives.interact_with_npc(dialogue), "9")
            ], (lambda : tutorial.enable_next_step())),
            Objective([
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_x), "10")
            ], (lambda : tutorial.enable_next_step())),
            Objective([
                Requirement(lambda state: Objectives.last_step_tutorial(tutorial), "11")
            ], (lambda : tutorial.enable_next_step()))
        ]
        self.current_objective = 0
        
        # Dropdown
        objetivos = [
            "Completa la misión A",
            "Recoge 10 elementos",
            "Habla con el NPC1"]
        self.button = Button()
        self.dropdown = Dropdown(self.button.rect, objetivos)
        self.hide_dropdown = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def evaluate(self):
        if self.current_objective < len(self.objectives) and self.objectives[self.current_objective].evaluate():
            self.current_objective += 1

    def show_dropdown(self, left_mouse_button_down, event):
        if left_mouse_button_down:
            if self.button.rect.collidepoint(event.pos):
                self.hide_dropdown = not self.hide_dropdown
                if self.hide_dropdown:
                    print('entro en update()')
                    self.dropdown.update_dimensions()

        self.button.draw(self.screen)
        if self.hide_dropdown:
            self.dropdown.draw(self.screen)


class Objective:
    def __init__(self, requirements, action):
        self.requirements = requirements
        self.action = action
        self.true_results = []

    def evaluate(self):
        result = [(requirement.get_id(), requirement.evaluate(self.true_results)) for requirement in self.requirements]
        self.true_results = [id for (id, boolean) in result if boolean]
        boolean_results = [boolean for (id,boolean) in result]
        if all(boolean_results):
            (self.action)()
            return True
        return False

class Requirement:
    def __init__(self, check, id, dependencies = []):
        self.check = check
        self.state = False
        self.id = id
        self.dependencies = dependencies

    def evaluate(self, true_results):
        # print(f" REQ{self.id}")
        if set(self.dependencies).issubset(set(true_results)):
            result = (self.check)(self.state)
            self.state = result
            return result
        return False

    def get_id(self):
        return self.id

class Button:
    def __init__(self):
        self.button_objetivos = pygame.image.load('./code/sprites/tutorial/objetivos.png')
        self.rect = self.button_objetivos.get_rect(topright=(SCREEN_WIDTH, 0))

    def draw(self, screen):
        screen.blit(self.button_objetivos, self.rect)

class Dropdown:
    def __init__(self, button_rect, items):
        self.button_rect = button_rect
        self.items = items
        self.image = pygame.image.load('./code/sprites/tutorial/dropdown.png')
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 20)
        self.boton_imagen = pygame.image.load('./code/sprites/tutorial/boton_lila.png')
        self.update_dimensions()

    def update_dimensions(self):
        # Calcular la altura del desplegable en función del contenido
        self.rect.width = max(self.font.size(item)[0] for item in self.items) + self.boton_imagen.get_width() + 20  # Añadir un margen de 20 # Ajustar el ancho para dar espacio suficiente al texto
        self.rect.height = min(len(self.items) * 30, SCREEN_HEIGHT - self.button_rect.bottom)  # Limitar la altura al espacio disponible

        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        # Posicionar el desplegable debajo del botón
        self.rect.top = self.button_rect.bottom
        self.rect.centerx = self.button_rect.centerx

        # Ajustar la posición del desplegable para que esté completamente dentro de la pantalla
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for i, item in enumerate(self.items):
            text_surface = self.font.render(item, True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(self.rect.x + self.boton_imagen.get_width() + 10, self.rect.y + 10 + i * 30))
            screen.blit(self.boton_imagen, (self.rect.x + 5, text_rect.y))  # Dibujar el botón a la izquierda
            screen.blit(text_surface, text_rect)
