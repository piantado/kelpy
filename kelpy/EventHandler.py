import pygame
from kelpy.Miscellaneous import *

"""
These functions are designed to be fed a kelpy OrderedUpdate list (as illustrated in the demos, usually named 'dos')
They are to be placed within the kelpy_standard_event_loop and will signal whether a mouse click has occurred (is_click), and what object was clicked (who_was_clicked).
"""

def is_click( event ):
	"""
	is_click can be run in the kelpy_standard_event_loop to detect mouse click events.
	if your for loop is written "for event in kelpy_standard_event_loop:" you can then use this function as follows:
	if is_click(event):
		*code for whatever you want to happen*
	"""
	if   (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
		return True
	else:
		return False

def who_was_clicked( things ):
	"""
	who_was_clicked can be run following an is_click event to return the object that was clicked.
	if isclick(event):
		thing_that_was_clicked = who_was_clicked(dos)
	
	Remembering that 'dos' just refers to the kelpy OrderedUpdate list.
	
	Keep in mind this function is not designed to handle clicks on multiple objects, ie if there are two sprites on top of each other, it will return the first one in the ordered updates list.
	This may mean the item on the bottom will be returned first, if it is in line to be checked first.
	
	"""
	for x in iter(things, ):
		if x.click_inside(pygame.mouse.get_pos()):
			return x

def was_dropped_into_zone( event, *args, **kwargs):
	"""
		This function returns true if an event in the event loop signals that a Drop ZONE_EVENT has taken place, ie. if a DragSprite has been dropped onto a registered DropSprite.
	"""
	if (event.type is ZONE_EVENT and event.motion=='drop' and event.direction =='enter'):
		return True

def who_was_dropped( event, **kwargs):
	"""
		if an event returns true in the funtion above, run this to return who was dropped.
	"""
	return event.obj
	