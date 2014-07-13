from CommandableSprite import CommandableSprite
import pygame
import pygame.font

class TextSprite(CommandableSprite):
	"""
		A class for displaying fonts. 
		Most of the image/surface processing is done at initialization, rather than in .draw(), in order
		to make drawing faster (for RSVP, etc)
	
	"""
	
	def __init__(self, text, screen, init_position, isdraggable=False):
		CommandableSprite.__init__(self, screen, init_position, isdraggable=isdraggable)
		self.font = pygame.font.Font(None, 36)
		self.set_text(text)

	def set_text(self, t):
		# store the string
		self.text = t 
		
		# and render it
		self.textrender = self.font.render(self.text, 1, (10, 10, 10))
		self.size = self.font.size(self.text) ## TODO: FIX THE SIZES
		
	def draw(self):
		w,h = self.size
		self.screen.blit(self.textrender, pygame.Rect(self.get_x() - w/2, self.get_y() - h/2, w, h) )
		