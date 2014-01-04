# -*- coding: utf-8 -*-

"""
	Just a cool demo for hysterisis in contrast sensitivity
"""

from kelpy.CommandableImageSprite import *
from kelpy.DisplayQueue import *
from kelpy.Miscellaneous import *
from kelpy.OrderedUpdates import *

## To record video of a display, just import this:
#import kelpy.ScreenVideoRecorder

##############################################
## Set up pygame

screen = initialize_kelpy(fullscreen=False) 

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
CENTER_STAGE  = ( WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

probe  = CommandableImageSprite( screen, CENTER_STAGE, kstimulus("cars/beetle.png"), scale=0.5)
fixation  = CommandableImageSprite( screen, CENTER_STAGE, kstimulus("fixation/blue_cross.png"), scale=0.3)
ou = OrderedUpdates(probe, fixation)

Q = DisplayQueue()
Q.append(obj=probe, action='wait',   duration=2)
Q.append(obj=probe, action='darken', amount=0.05, duration=3.0)
Q.append(obj=probe, action='wait',   duration=3)
Q.append(obj=probe, action='wait',   duration=5)
Q.append(obj='throw_event', event=pygame.event.Event(EXIT_KELPY_STANDARD_EVENT_LOOP))

for event in kely_standard_event_loop(screen, Q, ou): 	
	pass
