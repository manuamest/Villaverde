from os import walk
import pygame
import os

def import_folder(path):
	surface_list = []
	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)
	return surface_list

def load_frames(dir):      
        frame_files = sorted(os.listdir(dir), key=lambda x: int(x.split('.')[0]))
        frames = [pygame.image.load(os.path.join(dir, file)) for file in frame_files]
        return frames