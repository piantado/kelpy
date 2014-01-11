from pygame import Surface

class KelpyScreen(Surface):
	"""
	this class is going to take a pygame screen object and add some extra parameters to create a kelpy screen object.
	It does not work correctly, currently.
	"""
	
	def __init__(self, surface):
		"""
			This intilialization function takes in a pygame Surface object (will be created with the initilize_kelpy() function).
			It then wraps that Surface object into the KelpyScreenObject class that provides a place to store extra attributes.
			As it is, this class is pretty bare, but will have more functionality later.
		"""
		self.screen = surface
		self.HEIGHT = self.screen.get_height()
		self.WIDTH = self.screen.get_width()
	
	def fill(self, color):
		self.screen.fill(color)