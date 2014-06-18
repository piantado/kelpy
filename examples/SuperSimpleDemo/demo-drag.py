# -*- coding: utf-8 -*-

from kelpy.Miscellaneous import *
from kelpy.DragDrop import DragSprite
from kelpy.DisplayQueue import DisplayQueue
from kelpy.OrderedUpdates import OrderedUpdates
from kelpy.EventHandler import was_clicked, is_click

screen, locations = initialize_kelpy( dimensions=(800,600) )

a = DragSprite( screen, locations.east, kstimulus('animals/giraffe.png'), scale=0.25)

## What the image does
Q = DisplayQueue()
Q.append(obj=a, action='move',   pos=locations.center, duration=3.0)

# Create a list of things to display, update
objects = OrderedUpdates(a) 

## The standard event loop in kelpy -- this loops infinitely to process interactions
## and throws events depending on what the user does
for event in kelpy_standard_event_loop(screen, Q, objects):
	
	a.process_dragndrop(event)
	
	# If the event is a click:
	if is_click(event) and not was_clicked(a):
		Q.append(obj=a, action='waggle', duration=0.5, amount=1.0, period=0.25)
		