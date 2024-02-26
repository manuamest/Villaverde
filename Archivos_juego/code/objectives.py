import pygame


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
        print(inventory.is_empty())
        return not inventory.is_empty()
            
    def __init__(self, tutorial, inventory):
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
            ], (lambda : tutorial.enable_next_step()))
        ]
        self.current_objective = 0

    def evaluate(self):
        if self.current_objective < len(self.objectives) and self.objectives[self.current_objective].evaluate():
            self.current_objective += 1


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
        print(f" REQ{self.id}")
        if set(self.dependencies).issubset(set(true_results)):
            result = (self.check)(self.state)
            self.state = result
            return result
        return False

    def get_id(self):
        return self.id
