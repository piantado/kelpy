# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tobii sim controller for kelpy
#		this controller is intended to be used as a simple development tool to simulate 
#		gaze input from a tobii eye tracker. it returns a tuple of the mouse's position.
#		
#		this version does not simulate a full range of tobii data, like the validity codes or depth or anything fancy.
#
#		
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##this version uses nothing that the original uses.
import pygame
from pygame.locals import *


## This is a tobii simulator made mostly from bandaids and tape.


class TobiiSimController:

	def __init__(self, screen):
		self.screen = screen   
	
	def get_center_gaze( self ):
		# print pygame.mouse.get_pos()
		return (pygame.mouse.get_pos())
	
	def print_mouse_position(self):
		print (integer(pygame.mouse.get_pos()[0]),integer(pygame.mouse.get_pos9[1])) 
		