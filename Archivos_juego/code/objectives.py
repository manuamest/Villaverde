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
        
    def inventory_is_not_empty(state, inventory):
        if state:
            return True
        elif not inventory.is_empty():
            return True
        return False
    
    def interact_with_npc(dialogue):
        return dialogue.obtener_dialogo() == True
    
    def last_step_tutorial(tutorial):
        return tutorial.indice_tutorial == (len(tutorial.tutorial_mensajes) - 1)

            
    def __init__(self, screen, tutorial, inventory, dialogue, player, soil_layer, objective_index):
        self.objectives = [
            # Objectives del tutorial
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
                Requirement(lambda state: Objectives.inventory_is_not_empty(state, inventory), "7")
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
                Requirement(lambda state: self.click_on_objectives_button == True, "11")
            ], (lambda : tutorial.enable_next_step())),
            Objective([
                Requirement(lambda state: Objectives.last_step_tutorial(tutorial), "12")
            ], (lambda : tutorial.enable_next_step())),
            # Objectives (mapa verano) nivel 1
            Objective([
                Requirement(lambda state: player.is_cut_down_tree() == True, "13")
            ], (lambda : self.dropdown.set_check_button(0))),
            Objective([
                Requirement(lambda state: inventory.get_madera() == 3, "14"),
            ], (lambda : self.dropdown.set_check_button(1))),
            Objective([
                Requirement(lambda state: player.talk_with("mercader") == True, "15")
            ], (lambda : self.dropdown.set_check_button(2))),
            Objective([
                Requirement(lambda state: inventory.get_dinero() == 10, "16")
            ], (lambda : self.dropdown.set_check_button(3))),
            Objective([
                Requirement(lambda state: player.talk_with("butanero") == True, "17")
            ], (lambda : self.dropdown.set_check_button(4))),
            Objective([
                Requirement(lambda state: dialogue.obtener_dinero_dado() == True, "18")
            ], (lambda : self.dropdown.set_check_button(5))),
            Objective([
                Requirement(lambda state: player.talk_with("don diego") == True, "19")
            ], (lambda : self.dropdown.set_check_button(6))),
            # Objectives (mapa otoño) nivel 2
            Objective([
                Requirement(lambda state: soil_layer.get_fase_cultivo("plantar") == True, "20"),
                Requirement(lambda state: soil_layer.get_fase_cultivo("regar") == True, "21", ["20"])
            ], (lambda : self.dropdown.set_check_button(7))),
            Objective([
                Requirement(lambda state: inventory.get_trigo() >= 5 , "22")
            ], (lambda : self.dropdown.set_check_button(8))),
            Objective([
                Requirement(lambda state: player.talk_with("modista") == True, "23")
            ], (lambda : self.dropdown.set_check_button(9))),
            Objective([
                Requirement(lambda state: player.talk_with("gallina") == True, "24")
            ], (lambda : self.dropdown.set_check_button(10))),
            Objective([
                Requirement(lambda state: inventory.get_zapatillas() == 1, "25")
            ], (lambda : self.dropdown.set_check_button(11))),
            # Objectives (mapa invierno) nivel 3
            # Objectives (mapa lava) nivel 4
            # Objective([
            #     Requirement(lambda state: inventory.get_dinero() > 0, "14")
            # ], (lambda : self.dropdown.set_check_button(2)))
        ]
        # Indice del objetivo actual
        self.objective_index = objective_index
        self.current_objective = 0 if self.objective_index == None else self.objective_index
        
        # Dropdown
        objetivos = [
            ("Tala un arbol usando el hacha", False),   # Nivel 1
            ("Consigue 3 de madera", False),
            ("Habla con Xoel el Mercader", False),
            ("Consigue 10 moneda", False),
            ("Habla con Jordi, el obrero", False),
            ("Dale dinero a Jordi", False),
            ("Habla con Don Diego", False),
            ("Planta trigo y riegalo", False),    # Nivel 2
            ("Recoge 5 de trigo", False),
            ("Habla con Eva la modista", False),
            ("Habla con la gallina Daniel", False),
            ("Consigue las zapatillas de Daniel", False),
            # ("Consigue las gafas y bufanda de Isabel", False),
            # ("Consigue la gorra y bufanda de Oscar", False),
            # ("Consigue la gorrita Kimoa de Fer", False),
            # ("Resuelve el puzzle", False)         # Nivel4
            ]

        self.button = Button()
        self.dropdown = Dropdown(self.button.rect, objetivos)
        self.hide_dropdown = False
        self.screen = screen
        self.click_on_objectives_button = False

    def evaluate(self, allow_next_objective = True):
        if self.current_objective < len(self.objectives) and self.objectives[self.current_objective].evaluate() and allow_next_objective:
            self.current_objective += 1

    def show_dropdown(self, left_mouse_button_down, event):
        if left_mouse_button_down and self.button.rect.collidepoint(event.pos):
            self.hide_dropdown = not self.hide_dropdown
            self.click_on_objectives_button = True
            if self.hide_dropdown:
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
        self.button_objetivos = pygame.image.load('./code/sprites/objetivos/objetivos.png')
        self.rect = self.button_objetivos.get_rect(topright=(SCREEN_WIDTH, 0))

    def draw(self, screen):
        screen.blit(self.button_objetivos, self.rect)

class Dropdown:
    def __init__(self, button_rect, objectives):
        self.button_rect = button_rect
        self.objectives = objectives
        self.str_objectives = [obj for (obj,check_button) in objectives]
        self.dropdown_image = pygame.image.load('./code/sprites/objetivos/dropdown.png')
        self.rect_dropdown = self.dropdown_image.get_rect()
        self.font = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 20)
        self.image_check_button = pygame.image.load('./code/sprites/objetivos/boton_lila.png')
        self.update_dimensions()

    def update_dimensions(self):
        # Calcular la altura del desplegable en función del contenido
        self.rect_dropdown.width = max(self.font.size(obj)[0] for obj in self.str_objectives) + self.image_check_button.get_width() + 20
        self.rect_dropdown.height = min(len(self.str_objectives) * 30, SCREEN_HEIGHT - self.button_rect.bottom)  # Limitar la altura al espacio disponible

        self.dropdown_image = pygame.transform.scale(self.dropdown_image, (self.rect_dropdown.width, self.rect_dropdown.height))

        # Posicionar el desplegable debajo del botón
        self.rect_dropdown.top = self.button_rect.bottom
        self.rect_dropdown.centerx = self.button_rect.centerx

        # Ajustar la posición del desplegable para que esté completamente dentro de la pantalla
        if self.rect_dropdown.right > SCREEN_WIDTH:
            self.rect_dropdown.right = SCREEN_WIDTH
    
    def set_check_button(self, index):
        self.objectives[index] = (self.objectives[index][0], True)

    def draw(self, screen):
        screen.blit(self.dropdown_image, self.rect_dropdown.topleft)
        for i, (obj,check_button) in enumerate(self.objectives):
            self.image_check_button = pygame.image.load(f'./code/sprites/objetivos/{"boton_lila_ok" if check_button else "boton_lila"}.png')
            text_surface = self.font.render(self.str_objectives[i], True, (33, 10, 37))
            text_rect = text_surface.get_rect(topleft=(self.rect_dropdown.x + self.image_check_button.get_width() + 10, self.rect_dropdown.y + 5 + i * 30))
            screen.blit(self.image_check_button, (self.rect_dropdown.x + 5, text_rect.y))  # Dibujar el botón a la izquierda
            screen.blit(text_surface, text_rect)
