
# Let's make just colored circle regions for drag and drop onto.
# Each one does a thing --either changing size or shape
# and each you can drag the "invert" ring (a border) that will make it do the opposite. 


# -*- coding: utf-8 -*-

from random import randint, choice, sample, shuffle
from time import time

from kelpy.CommandableSprites import *
from kelpy.DisplayQueue import *
from kelpy.Miscellaneous import *
from kelpy.OrderedUpdates import *

## To record video of a display, just import this:
#import kelpy.ScreenVideoRecorder

##############################################
## Set up pygame

#screen = initialize_kelpy(fullscreen=True) 
screen = initialize_kelpy(fullscreen=False) 

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
CENTER_STAGE  = ( WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

box1 = CommandableImageSprite( screen, (WINDOW_WIDTH/3,   WINDOW_HEIGHT-200)  , kstimulus("circle_solid_red.png"),  scale=0.5)
box2 = CommandableImageSprite( screen, (2*WINDOW_WIDTH/3,   WINDOW_HEIGHT-200), kstimulus("circle_solid_blue.png"), scale=0.5)

obj = CommandableImageSprite( screen, (0,0), kstimulus("beetle.png"), scale=0.15, isdraggable=True)
ring  = CommandableImageSprite( screen, CENTER_STAGE, kstimulus("circle_dotted_outline_green.png"), scale=0.5, isdraggable=True)

# define drop zones, which in turn trigger ZONE_EVENT when registered objects are dragged/dropped onto them
obj.register_drop_zone(box1)
obj.register_drop_zone(box2)

ring.register_drop_zone(box1)
ring.register_drop_zone(box2)

ou = OrderedUpdates(box1, box2, obj, ring)

Q = DisplayQueue()

invert1 = False; # do we invert?
invert2 = False; # do we invert?

for event in kely_standard_event_loop(screen, Q, ou):
	
	## Process drag events to these
	## NOTE: we must give all events since they use mouseup and mousedown as well as mousemotion
	# this queues up ZONE_EVENTs which can then be processed below
	ou.process_dragndrop(event)
	
	if event.type is ZONE_EVENT:
		Q.append(obj='call', function=event.obj.disable_dragging )
		
		if event.obj is ring: # if we drag the capture
			if event.direction is "enter":
				if event.zone is box1: # if we drag onto the box1
					Q.append(obj=event.obj, action='move', duration=0.10, pos=box1.position() )
					invert1 = True
				elif event.zone is box2: # if we drag onto box 2
					Q.append(obj=event.obj, action='move', duration=0.10, pos=box2.position() )
					invert2 = True
			if event.direction is "exit": # any exit event, and nothing is inverted
				invert1 = False
				invert2 = False
				
		elif event.obj is obj:
			Q.append(obj=event.obj, action='move', duration=0.10, pos=event.zone.position() )
			
			## But what we do inside changes
			if   event.zone is box1: 
				if invert1: Q.append(obj=event.obj, action='spin', duration=1.0, amount=60)
				else      : Q.append(obj=event.obj, action='spin', duration=1.0, amount=-60)
				
			elif event.zone is box2: 
				if invert2: Q.append(obj=event.obj, action='scale', amount=0.7)
				else      : Q.append(obj=event.obj, action='scale', amount=1.0/0.7)
				
			Q.append(obj=event.obj, action='move', duration=0.20, pos=(event.zone.x, event.zone.y-200) )
				
		#print event

		Q.append(obj='call', function=event.obj.enable_dragging )
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
