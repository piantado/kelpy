from CommandableSprite import *
from pygame.image import *
import PIL.Image # we use this to load images so we can alter attributes easily
import PIL.ImageEnhance
import Image
from copy import deepcopy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This extends sprites by making them commandable, so that they will do things at certain times
# (in a sequence)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
class CommandableImageSprite(CommandableSprite):
	
	def __init__(self, screen, init_position, imagepath, rotation=0, scale=1.0, brightness=1.0, isdraggable=False):
		""" Create a new object.
		
		screen: 
		The screen on which the creep lives (must be a 
		pygame Surface object, such as pygame.display)
		
		init_position:
		A vec2d or a pair specifying the initial position
		of the creep on the screen.
		"""
		CommandableSprite.__init__(self, screen, init_position, isdraggable=isdraggable)
		
		
		# load the image
		##NOTE: Here image stores the current display image, and base_image stores it before scaling+rotation
		self.scale = scale
		self.rotation = rotation
		self.initial_scale = scale # for 'restore' command
		self.initial_rotation = rotation
		self.initial_brightness = brightness
		self.initial_imagepath = imagepath
		
		self.set_image(imagepath, rotation, scale, brightness)
		self.visible = True
		
		# some variables needed for the movements, to be stored across updates
		self.last_blink_parity = 1;
		
	
	def set_image(self, imagepath, rotation=0, scale=1.0, brightness=1.0):
		# We use PIL to load images (so we can manipulate them)
		self.PILimage = PIL.Image.open(imagepath)
		#self.PILimage = self.PILimage.resize(self.PILimage.size, Image.ANTIALIAS) # Hmm we should antialias here in the future
		assert self.PILimage.mode in ["RGB", "RGBA"], "*** NOT IN RIGHT MODE:"+self.PILimage.mode # check that its the right mode
		
		self.base_pyimage =  pygame.image.fromstring(self.PILimage.tostring(), self.PILimage.size, self.PILimage.mode)
		#self.base_image = pygame.image.load(imagepath).convert_alpha()
		self.image_path = imagepath
		
		# and update the features
		self.set_image_attributes(rotation=rotation, scale=scale, brightness=brightness)
		
	def set_image_attributes(self, rotation=None, scale=None, brightness=None):
		"""
			update the image attributes. Note: This does not load it from the disk -- it only re-loads from the PIL stored self.PILimage
		"""
		if rotation is None: rotation = self.rotation
		if scale is None:    scale    = self.scale
		
		if brightness is not None:
			# re-convert from PIL if we must (if brightness is altered)
			## NOTE: Wow this looks terrible, PIL. We'll write our own below
			#ii = PIL.ImageEnhance.Brightness(self.PILimage).enhance(brightness)
			#self.base_pyimage = pygame.image.fromstring(ii.tostring(), ii.size, ii.mode)
			
			#ii = PIL.Image.blend(PIL.Image.new(self.PILimage.mode, self.PILimage.size, 0), self.PILimage, brightness)
			
			ii = PIL.Image.eval(self.PILimage, lambda x: x*brightness)
			#ii = PIL.Image.eval(self.PILimage, lambda x: 0)
			#print brightness, ii.getpixel( (100,100) )
			self.base_pyimage = pygame.image.fromstring(ii.tostring(), ii.size, ii.mode)
		
		# re-rotate and zoom the base pyimage
		self.display_image = pygame.transform.rotozoom(self.base_pyimage, rotation, scale )
		w,h = self.display_image.get_size()	
		self.set_width(w)
		self.set_height(h)
		
		# and save the features
		self.scale = scale
		self.rotation = rotation
		if brightness is not None: self.brightness = brightness
		
		
	def update_action(self, **c):
		"""
			This is given c['finish']=True when we are done with this (so everythign should be snapped to final position)
		"""
		# try updating as a parent -- this defines self.start_x, self.start_y
		if CommandableSprite.update_action(self, **c): return True
		
		if c['first']: # If this is the first function call
			#self.start_x, self.start_y = self.position() # these are set above
			self.start_rotation = self.rotation
			self.start_scale = self.scale
			self.start_brightness = self.brightness
			
			
		action = c['action']
		duration = c.get('duration', 0.0) # get the duration else 0.0 if none is specified
		t = 1.0 if duration == 0.0 else (time() - c['start_time']) / float(duration) # what percent of the way through are we?
		
		# update according to remaining time
		if action == 'wagglemove': # waggle and move; should be a better way to do this
			x,y = c['pos']
			
			self.set_image_attributes(rotation=self.rotation + c['amount'] * sin(2.0 * pi * t / c['period']) / 2)
			
			self.set_x( (x - self.start_x) * t + self.start_x)
			self.set_y( (y - self.start_y) * t + self.start_y)
			
			if c.get('finish',False) is True: 
				self.set_position(c['pos']) # make sure you end up somewhere
				self.set_image_attributes(rotation=self.start_rotation)
		elif action == 'waggle': ## NOTE: this leaves it rotated if 
			self.set_image_attributes(rotation=self.rotation + c['amount'] * sin(2.0 * pi * t / c['period']) / 2)
			if c.get('finish',False) is True: self.set_image_attributes(rotation=self.start_rotation)
		elif action == 'circlescale':
			self.set_image_attributes(scale=self.scale + c['amount'] * sin(2.0 * pi * t / c['period'] ) / 2)
			if c.get('finish',False) is True: self.set_image_attributes(scale=self.start_scale)
		elif action == 'scale':
			self.set_image_attributes(scale=self.start_scale*(1.-t) + self.start_scale * c['amount'] * t)
			if c.get('finish',False) is True: self.set_image_attributes(scale=self.start_scale * c['amount'])
		elif action == 'swap': # here we swap the image for something else; parameters are scale and rotation
			# This can take a "flag" which is a global variable -- we only swap if the variable is "true" at the time this is evaled
			# if no flag is specified, we always do the swap
			self.set_image( c['image'], c['rotation'], c['scale'] ) # takes the file, rotation, scale from parameters
		elif action == 'rotate': # spin is an interactive action that takes some time
			self.set_image_attributes(rotation=self.start_rotation + t * c['amount'] )
		elif action == 'darken':
			self.set_image_attributes(brightness=self.start_brightness*(1.-t)+self.start_brightness*c['amount']*t)
			if c.get('finish',False) is True: self.set_image_attributes(brightness=self.start_brightness*c['amount'])
		elif action == 'swapblink': # swap between two images
			if c['first']: # if we are just starting this
				self.initial_swap_image = self.image_path
				self.initial_scale = self.scale
				self.initial_rotation = self.rotation
				self.initial_brightness = self.brightness
		
			period = c['period']
			t = (time() - c['start_time']) 
			parity = (1-abs((floor( t / period ) % 2)) < 1e-4) # make a number
			#print [t, period, self.last_blink_parity]
			
			if self.last_blink_parity != parity:
				self.last_blink_parity = parity
				if parity: self.set_image(self.initial_swap_image, self.initial_rotation, self.initial_scale)
				else:      self.set_image(c['image'], c['rotation'], c['scale'], c['brightness']) 				
		elif action == 'restore': # return to the original image that we loaded
			self.set_image(self.initial_imagepath, self.initial_rotation, self.initial_scale, self.initial_brightness)
		else: # if the parent could not update this
			print "*** Bad CommandableImageSprite action! ", action
			return False
			
		return True
		
		
	def draw(self):
		## here is where we process commands
		#print self.pos
		if self.visible:
			w = self.display_image.get_width()
			h = self.display_image.get_height()
			self.screen.blit(self.display_image, pygame.Rect(self.get_x() - w/2, self.get_y() - h/2, w, h)) # transform by our coordinates and draw

	def get_size_xy(self):
		## returns the image size and x/y spots as a tuple. **Width, Height**
		
		return self.display_image.get_width(), self.display_image.get_height(), self.get_x() , self.get_y()
	