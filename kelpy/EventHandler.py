import pygame
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *


def isClick( event ):
	if   (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
		return True
	else:
		return False

def wasClicked( things ):
	for x in iter(things, ):
		if x.click_inside(pygame.mouse.get_pos()):
			return x
	else:
		pass
	