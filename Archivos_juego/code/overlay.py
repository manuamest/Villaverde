import pygame
from settings import *

class Overlay:
    def __init__(self,player):
        
        # setup general
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports para el overlay
        overlay_path = './code/sprites/overlay/'
        # Asocia cada herramienta con su imagen
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seed}

        # Ajusta el tamaño de las imágenes de las semillas
        self.seeds_surf = {seed: pygame.transform.scale(image, (40,40)) for seed, image in self.seeds_surf.items()}
    
    def display(self):
        # Herramientas
        tool_surf = self.tools_surf[self.player.selected_tool]
        # Se situan las herramientas en la posicion indicada en el archivo settings
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # Semillas
        seed_surf = self.seeds_surf[self.player.selected_seed]
        # Se situan las semillas en la posicion indicada en el archivo settings
        seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)