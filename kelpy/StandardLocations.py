import pygame
from pygame.locals import *

class StandardLocations():
		"""
		This class can be used to call offscreen and onscreen locations to position things on a screen.
		It is used by the following code:
		screen = initialize_kelpy( dimensions=(800,600) ) ## INITIALIZE THE SCREEN OBJECT...
		spots = Spots(screen) ## FEED THE SCREEN OBJECT TO THE StandardLocations OBJECT...
		print spots.west ## YOU CAN NOW CALL THE POSITIONS FROM THE OBJECT AS ATTRIBUTES! YAY!
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
		
		## 4 spots along the screen from right to left (1-4)
		## and 4 rows top to bottom (a-d)
		self.a1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*1 )
		self.a2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*1 )
		self.a3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*1 )
		self.a4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*1 )

		self.b1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*2 )
		self.b2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*2 )
		self.b3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*2 )
		self.b4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*2 )

		self.c1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*3 )
		self.c2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*3 )
		self.c3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*3 )
		self.c4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*3 )
		
		self.d1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*4 )
		self.d2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*4 )
		self.d3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*4 )
		self.d4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*4 )

		# middle row spots
		self.midrow1 = ((screen.get_width() /5 ) * 1, (screen.get_height() /2 ) )
		self.midrow2 = ((screen.get_width() /5 ) * 2, (screen.get_height() /2 ) )
		self.midrow3 = ((screen.get_width() /5 ) * 3, (screen.get_height() /2 ) )
		self.midrow4 = ((screen.get_width() /5 ) * 4, (screen.get_height() /2 ) )

		#middle column spots
		self.midcol1 = ((screen.get_width() /2 ), (screen.get_height() /5 ) * 1)
		self.midcol2 = ((screen.get_width() /2 ), (screen.get_height() /5 ) * 2)
		self.midcol3 = ((screen.get_width() /2 ), (screen.get_height() /5 ) * 3)
		self.midcol4 = ((screen.get_width() /2 ), (screen.get_height() /5 ) * 4)

		self.center = ((screen.get_width() /2 ), (screen.get_height() /2 ) )
		self.cu=((screen.get_width() /2 ), (screen.get_height() /5)*1 )
		self.cd=((screen.get_width() /2 ), (screen.get_height()/5)*3 )