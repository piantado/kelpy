import os, sys
import pygame
from random import randint, choice, sample, shuffle
import numpy as np
from time import time

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *



IMAGE_SCALE = 0.25

MAX_DISPLAY_TIME = 12.0

##############################################
## Set up pygame

screen, spot = initialize_kelpy( dimensions=(850,600) )


OFF_SOUTH = (spot.south)
LID_SPOT1 = (((screen.get_width()/5) * 1)+25, (screen.get_height()/5)*3 )
LID_SPOT2 = (((screen.get_width()/5) * 4)+25, (screen.get_height()/5)*3 )
LID1_MOVE = (((screen.get_width()/5) * 1)+25, ((screen.get_height()/5)-50)*3 )
LID2_MOVE = (((screen.get_width()/5) * 4)+25, ((screen.get_height()/5)-50)*3 )


def present_trial(objects, probabilities, trial_duration, when_open):
    start_time = time()

    box1 =  CommandableImageSprite( screen, spot.c1, kstimulus("misc/box.png"), scale=1.2)
    boxfront1 = CommandableImageSprite(screen, spot.c1, kstimulus("misc/boxfront.png"), scale=1.2)
    lid1 =  CommandableImageSprite( screen, LID_SPOT1, kstimulus("misc/lid.png"), scale=1.2)
    box2 = CommandableImageSprite(screen, spot.c4, kstimulus("misc/box.png"), scale=1.2)
    boxfront2 = CommandableImageSprite(screen, spot.c4, kstimulus("misc/boxfront.png"), scale=1.2)
    lid2 = CommandableImageSprite(screen, LID_SPOT2, kstimulus("misc/lid.png"), scale=1.2)
    obj1 = CommandableImageSprite( screen, spot.c1, objects[0], scale=1.0)
    obj2 = CommandableImageSprite(screen, spot.c4, objects[1], scale=1.0)


    #the boxes keep opening every when_open seconds, and object appearance is stochastic

    # A queue of animation operations
    Q = DisplayQueue()

    Q.append(obj=lid1, action='wait', duration=when_open)
    Q.append(obj=lid2, action='wait', duration=when_open)
    Q.append_simultaneous(obj=lid1, action = 'move', pos=LID1_MOVE, duration=0.5)
    Q.append_simultaneous(obj=lid2, action='move', pos=LID2_MOVE, duration=0.5)
    #Q.append(obj=obj1, action='wait', duration=0.0)
    #Q.append(obj=obj2, action='wait', duration=0.0)

    #with certain probability, reveal object:
    flip1 = random.random()
    print flip1
    if  flip1 < probabilities[0]:
        Q.append_simultaneous(obj=obj1, action='move', pos=spot.b1, duration=1.0)

    #with other probability, reveal object
    flip2 = random.random()
    print flip2
    if flip2 < probabilities[1]:
        Q.append_simultaneous(obj=obj2, action='move', pos=spot.b4, duration=1.0)
    #Q.append_simultaneous(obj=obj1, action='move', pos=spot.b1, duration=1.0)

    Q.append(obj=obj1, action='wait', duration=1.0)
    Q.append(obj=obj2, action='wait', duration=1.0)

    Q.append(obj=lid1, action='wait', duration=1.0)
    Q.append(obj=lid2, action='wait', duration=1.0)

    Q.append_simultaneous(obj=obj1, action='move', pos=spot.c1, duration=1.0)
    Q.append_simultaneous(obj=obj2, action='move', pos=spot.c4, duration=1.0)
    Q.append_simultaneous(obj=lid1, action='move', pos=LID_SPOT1,duration=1.0)
    Q.append_simultaneous(obj=lid2, action='move', pos=LID_SPOT2, duration=1.0)

    Q.append(obj=obj1, action='move', pos=OFF_SOUTH, duration=0.0)
    Q.append(obj=obj2, action='move', pos=OFF_SOUTH, duration=0.0)

    # What order do we draw sprites and things in?
    dos = OrderedUpdates([box1,obj1,boxfront1, box2,obj2,boxfront2,lid1,lid2])  # Draw and update in this order

    for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):

        if (time() - start_time > MAX_DISPLAY_TIME):
            break

        # If the event is a click:
        if is_click(event):
            break





probs = [0.1, 0.25, 0.5, 0.75, 0.9]
objects = [kstimulus("misc/tennis.png") ,
kstimulus("misc/teddy.png"),kstimulus("misc/bug.png"),kstimulus("misc/duck.png"),kstimulus("misc/firetruck.png"),kstimulus("misc/robot.png")]

WHEN_OPEN = 2
TRIAL_DURATION = 30

import itertools
from random import shuffle

condition_set = set()
for i in itertools.combinations(probs,2):
    condition_set.add(i)
    condition_set.add(i[::-1])
conditions = list(condition_set)
print conditions
shuffle(conditions)


for cond in conditions:

    print ">>> Box 1 contains object with "+ str(cond[0])
    print ">>> Box 2 contains object with " + str(cond[1]) +"\n"
    random_stim = np.random.choice(objects, 2, replace=False)

    # calculate how many times to run the box_open
    for i in range(4):

        present_trial(random_stim, cond, TRIAL_DURATION, WHEN_OPEN)

    # new condition here