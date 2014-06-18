import pygame
from pygame.locals import *

class StandardLocations():
	"""
		This class can be used to call offscreen and onscreen locations to position things on a screen.
		It is used by the following code:
		screen = initialize_kelpy( dimensions=(800,600) )  ## INITIALIZE THE SCREEN OBJECT...
		spots = Spots(screen)   ## FEED THE SCREEN OBJECT TO THE StandardLocations OBJECT...
		print spots.west	## YOU CAN NOW CALL THE POSITIONS FROM THE OBJECT AS ATTRIBUTES! YAY!
	"""
	def __init__(self, screen):
		"""
			This initializes everything.
		"""
		## offscreen spots


		self.west = ( -screen.get_width(),  screen.get_height() /2 )
		self.northwest = ( -screen.get_width(), -screen.get_height() )
		self.north = ( screen.get_width()/2, -screen.get_height() )
		self.northeast = ( screen.get_width() *2, -screen.get_height() )
		self.east = ( screen.get_width() * 2, screen.get_height()/2 )
		self.southeast= ( screen.get_width() * 2, screen.get_height() * 2 )
		self.south = ( screen.get_width()/2 , screen.get_height() * 2 )
		self.southwest = ( -screen.get_width(), screen.get_height()*2 )
		
		## 4 spots along the screen from right to left
		self.a1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*2 )
		self.a2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*2 )
		self.a3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*2)
		self.a4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*2 )
		#used to be topq1... etc

		self.b1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*3 )
		self.b2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*3 )
		self.b3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*3 )
		self.b4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*3 )
		
		self.c1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*4 )
		self.c2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*4 )
		self.c3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*4 )
		self.c4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*4 )


		self.center = ((screen.get_width() /2 ), (screen.get_height() /2 ) )