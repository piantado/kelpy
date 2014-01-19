from kelpy.CommandableImageSprite import *
from kelpy.Dragable import *

class DragSprite(CommandableImageSprite, Dragable):
	"""
		The DragSprite is used to create a dragable sprite. It is written so that you feed it similar parameters that you would feed a regualar CommandableImageSprite.
		The only difference is that this sprite is able to be dragged around, once the drag and drop function is run in the main event loop (object.process_dragndrop(event))
	"""
	def __init__(self, canvas, initial_position, imgpath, rotation=0, scale=.20):
		CommandableImageSprite.__init__(self, canvas, initial_position, imgpath, rotation, scale)
		Dragable.__init__(self)
		self.set_x(initial_position[0])
		self.set_y(initial_position[1])
		self.set_height(self.display_image.get_height())
		self.set_width(self.display_image.get_width())
	


class DropSprite(CommandableImageSprite, Arrangeable):
	"""
		The DropSprite class is used to create a sprite with a drop zone on top of it. You then register the drop zone via the DragSprite.register_drop_zone(DropSprite) line.
		
	"""
	def __init__(self, canvas, initial_position, imgpath, rotation=0, scale=.20):
		CommandableImageSprite.__init__(self, canvas, initial_position, imgpath, rotation, scale)
		Arrangeable.__init__(self)
		self.set_x(initial_position[0])
		self.set_y(initial_position[1])
		self.set_height(self.display_image.get_height())
		self.set_width(self.display_image.get_width())
