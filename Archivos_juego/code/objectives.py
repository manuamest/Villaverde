import pygame
from settings import *

class Objectives:

    def __init__(self, screen, inventory, dialogue, player, soil_layer, opcion_mapa):
        self.salir_escena = False
        objectives_check_n1 = [
            # nivel 1
            Objective([
                Requirement(lambda state: player.talk_with("don diego") == True, "0")
            ], (lambda : self.dropdown.set_check_button(0))),
            Objective([
                Requirement(lambda state: player.talk_with("butanero") == True, "1")
            ], (lambda : self.dropdown.set_check_button(1))),
            Objective([
                Requirement(lambda state: inventory.get_dinero() == 100, "2")
            ], (lambda : self.dropdown.set_check_button(2))),
            Objective([
                Requirement(lambda state: player.is_cut_down_tree() == True, "3")
            ], (lambda : self.dropdown.set_check_button(3))),
            Objective([
                Requirement(lambda state: inventory.get_madera() >= 20 , "4"),
            ], (lambda : self.dropdown.set_check_button(4))),
            Objective([
                #Requirement(lambda state: dialogue.get_objetos_a_jordi() == True, "5")
            ], (lambda : self.dropdown.set_check_button(5)))
            ]
        objectives_check_n2 = [
            Objective([
                Requirement(lambda state: soil_layer.get_fase_cultivo("arar") == True, "0"),
            ], (lambda : self.dropdown.set_check_button(0))),
            Objective([
                Requirement(lambda state: soil_layer.get_fase_cultivo("sembrar") == True, "1"),
            ], (lambda : self.dropdown.set_check_button(1))),
            Objective([
                Requirement(lambda state: soil_layer.get_fase_cultivo("regar") == True, "2")
            ], (lambda : self.dropdown.set_check_button(2))),
            Objective([
                Requirement(lambda state: inventory.get_trigo() >= 1 , "3")
            ], (lambda : self.dropdown.set_check_button(3))),
            Objective([
                Requirement(lambda state: player.talk_with("mercader") == True, "4")
            ], (lambda : self.dropdown.set_check_button(4))), 
            Objective([
                Requirement(lambda state: player.talk_with("modista") == True, "5")
            ], (lambda : self.dropdown.set_check_button(5))),
            Objective([
                Requirement(lambda state: player.talk_with("pollo") == True, "6")
            ], (lambda : self.dropdown.set_check_button(6))),
            Objective([
                Requirement(lambda state: player.talk_with("oveja") == True, "7")
            ], (lambda : self.dropdown.set_check_button(7))),
            Objective([
                Requirement(lambda state: player.talk_with("vaca") == True, "8")
            ], (lambda : self.dropdown.set_check_button(8))),
            # Objective([
            #     Requirement(lambda state: , "9")
            # ], (lambda : self.dropdown.set_check_button(9))),
            ]
        
        objectives_check_n3 = [
            Objective([
                Requirement(lambda state: inventory.get_llave() == 1, "1")
            ], (lambda : self.dropdown.set_check_button(0)))]

        # Dropdown
        objetivos_n1 = [("Habla con Don Diego", False),
                        ("Habla con Jordi el obrero", False),
                        ("Consigue el dinero", False),
                        ("Tala un arbol usando el hacha (SPACE)", False),
                        ("Consigue 20 de madera", False),
                        ("Dale a Jordi lo que necesita", False)
                        ]
        objetivos_n2 = [("Ara la tierra con la azada (SPACE)", False),
                        ("Planta trigo (F)", False),
                        ("Usa la regadera (SPACE)", False),
                        ("Recoge trigo", False),
                        ("Habla con Xoel el Mercader", False),
                        ("Habla con Eva la modista", False),
                        ("Habla con la gallina Daniel", False),
                        ("Habla con la oveja Óscar", False),
                        ("Habla con la vaca Klara", False),
                        # ("Haz que todos los animales sean felices de nuevo", False)
                        ]
        objetivos_n3 = [("Consigue la llave magistral", False)]

        self.opcion_mapa = opcion_mapa
        if self.opcion_mapa == "verano":
            self.objectives_check = objectives_check_n1
            self.objectives = objetivos_n1
        elif self.opcion_mapa == "otoño":
            self.objectives_check = objectives_check_n2
            self.objectives = objetivos_n2
        elif self.opcion_mapa == "invierno":
            self.objectives_check = objectives_check_n3
            self.objectives = objetivos_n3

        self.hide_dropdown = False
        self.screen = screen
        self.click_on_objectives_button = False
        self.button = Button()
        self.dropdown = Dropdown(self.button.rect, self.objectives)

    def evaluate(self):
        nivel_completo = all(obj.evaluate() for obj in self.objectives_check)  # Verifica si todos los objetivos del nivel están completos
        if nivel_completo:
            self.salir_escena = True  # Establece salir_escena en True si todos los objetivos del nivel 1 están completos
            print("SALIR DE ESCENA:", self.salir_escena)
        for i in range(len(self.objectives)):
            self.objectives_check[i].evaluate()

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
        self.completed = False

    def evaluate(self):
        result = [(requirement.get_id(), requirement.evaluate(self.true_results)) for requirement in self.requirements]
        self.true_results = [id for (id, boolean) in result if boolean]
        boolean_results = [boolean for (id,boolean) in result]
        if all(boolean_results) and not self.completed:  # Verifica si todos los requisitos son verdaderos y el objetivo no se ha completado previamente
            (self.action)()
            self.completed = True  # Marca el objetivo como completado
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
