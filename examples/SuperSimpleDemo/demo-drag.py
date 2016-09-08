# -*- coding: utf-8 -*-

from kelpy.Miscellaneous import *
from kelpy.DragDrop import DragSprite
from kelpy.DisplayQueue import DisplayQueue
from kelpy.EventHandler import was_clicked, is_click

screen, locations = initialize_kelpy( dimensions=(800,600) )

myobject = DragSprite( screen, locations.east, kstimulus('animals/giraffe.png'), scale=0.25)

## What the image does
Q = DisplayQueue() # a list of things that happen
Q.append(obj=myobject, action='move', pos=locations.center, duration=2.0)

## The standard event loop in kelpy -- this loops infinitely to process interactions
## and throws events depending on what the user does
for event in kelpy_standard_event_loop(screen, Q, myobject):
	
	# If we want to process drag and drops
	# myobject.process_dragndrop(event)
	
	if is_click(event) and not was_clicked(myobject):
		Q.append(obj=myobject, action='waggle', duration=0.5, amount=1.0, period=0.25)
	
	pass
	
	