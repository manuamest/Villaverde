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
            
    def __init__(self):
        self.objectives = [
            Objective([
                Requirement(lambda state: Objectives.is_key_pressed(state, pygame.K_w))
            ], (lambda: print("OBJETIVE[[[[[[[]]]]]]]]]]]]]]")))
        ]
        self.current_objective = 0

    def evaluate(self):
        self.objectives[self.current_objective].evaluate()


class Objective:
    def __init__(self, requirements, action):
        self.requirements = requirements
        self.action = action

    def evaluate(self):
        if all(requirement.evaluate() for requirement in self.requirements):
            (self.action)()


class Requirement:
    def __init__(self, check):
        self.check = check
        self.state = False

    def evaluate(self): 
        result = (self.check)(self.state)
        self.state = result
        return result
