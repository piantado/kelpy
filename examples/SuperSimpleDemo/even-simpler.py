# -*- coding: utf-8 -*-

from kelpy.Miscellaneous import *
from kelpy.DragDrop import DragSprite
from kelpy.DisplayQueue import DisplayQueue
from kelpy.OrderedUpdates import OrderedUpdates
from kelpy.EventHandler import was_clicked, is_click

screen, locations = initialize_kelpy( dimensions=(800,600) )

a = DragSprite( screen, locations.center, kstimulus('animals/giraffe.png'), scale=0.25)

## Create a list of things to display, update
objects = OrderedUpdates(a) 

### The standard event loop in kelpy -- this loops infinitely to process interactions
### and throws events depending on what the user does
for event in kelpy_standard_event_loop(screen, objects):
	
	pass