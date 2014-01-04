import pygame
from kelpy.Miscellaneous import *

def is_click( event ):
	if   (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
		return True
	else:
		return False

def who_was_clicked( things ):
	for x in iter(things, ):
		if x.click_inside(pygame.mouse.get_pos()):
			return x