
"""
	
"""

from Arrangeable import *
from Miscellaneous import *


class Dragable(Arrangeable):
	"""
	A dragable is a kind of arrangeable, but supports drag and drop
	It also maintains a list of "event zones" which are areas where an event will be
	triggered if it is drag and/or dropped into
	"""
	
	def __init__(self):
		Arrangeable.__init__(self)
	
		## for drag and drop suport
		self.clickstart = None  # where were we when the clicking started?
		self.isdragging = False # are we currently being dragged?
		self.can_we_drag = True
		
		self.drag_zones = []
		self.drop_zones = []
		
	def register_drag_zone(self, z):
		"""
			This will make our dragndrop track the location of z, and when we drag onto it, 
			we post a ZONE_EVENT via process_dragndrop
			
			z - any Arrangeable. 
		"""
		self.drag_zones.append(z)
		
	def register_drop_zone(self, z):
		"""
			This will make our dragndrop track the location of z, and when we drop onto it, 
			we post a ZONE_EVENT via process_dragndrop
			
			z - any Arrangeable. 		"""
		self.drop_zones.append(z)
	
	def set_draggable(self,v):
		if v: self.enable_dragging()
		else: self.disable_dragging()
	
	def disable_dragging(self):
		"""
			Prevent drag-n-drop on this
			This just makes sure we aren't currently dragging
		"""
		self.can_we_drag = False
		self.isdragging = False

	def enable_dragging(self):
		"""
			Allow drag-n-drop on this
		"""
		self.can_we_drag = True
		self.isdragging = False
		
	def process_dragndrop(self, event):
		"""
			Pass this all kelpy events and it handles drag and drop. 
			
			When something enters or exits a registered zone, this posts a ZONE_EVENT to pygame.event.Event, with 
			the following features:
			motion: drag or drop
			direction: enter or exit (a zone)
			obj:  who did the moving
			zone: what the zone is
			
			This then returns true if we are currently dragging. 
		"""
		
		# if we can't even drag, get the hell out of here
		if self.can_we_drag is False: return False
		
		# if there is an event in there
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.click_inside(event.pos):
				self.isdragging = True
				self.clickstart = self.position()
				return True # we are dragging!
			else:   return False
			
		elif self.isdragging:
			
			# Process drag
			if event.type == pygame.MOUSEMOTION:
				newpos = self.get_x() + event.rel[0] , self.get_y() + event.rel[1] 
				
				for z in self.drag_zones:
					wasinz = z.is_inside( (self.x, self.y) )
					nowinz = z.is_inside(newpos)
					if (not wasinz) and nowinz: # the first time you enter
						pygame.event.post(pygame.event.Event(ZONE_EVENT, motion="drag", direction="enter", obj=self, zone=z))
					if wasinz and (not nowinz): # first time you exit
						pygame.event.post(pygame.event.Event(ZONE_EVENT, motion="drag", direction="exit", obj=self, zone=z))
					
				self.set_x( newpos[0] )
				self.set_y( newpos[1] )
			
				return True

			# Process drop
			if event.type == pygame.MOUSEBUTTONUP:
				self.isdragging=False
				
				for z in self.drop_zones:
					nowinz = z.is_inside( (self.x, self.y) )
					wasinz = z.is_inside( self.clickstart )
					
					if (not wasinz) and nowinz: # drop inside
						pygame.event.post(pygame.event.Event(ZONE_EVENT, motion="drop", direction="enter", obj=self, zone=z))
					if wasinz and (not nowinz): # drop outside
						pygame.event.post(pygame.event.Event(ZONE_EVENT, motion="drop", direction="exit", obj=self, zone=z))
					
				
				return False
			
		return False
		
	def update(self):
		Arrangeable.update(self) # call the update
	
	#def easy_setup(self, (w, h, x, y)):
		#self.set_x(x)
		#self.set_y(y)
		#self.set_height(h)
		#self.set_width(w)