import os, sys
import pygame
from random import randint, choice, sample, shuffle
from time import time

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *

IMAGE_SCALE = 0.10

MAX_DISPLAY_TIME = 5.0

##############################################
## Set up pygame

screen, spot = initialize_kelpy(dimensions=(800, 600))

OFF_LEFT = (spot.west)

# 4 quadrants, each with possible positions
quadrant1 = [spot.a1,spot.a2, spot.b1,spot.b2]
quadrant2 = [spot.a3,spot.a4, spot.b3, spot.b4]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(image, position):
    """
    This is the main function used to run this demo. It is fed an imagepath and uses this to create a CommandableImageSprite offscreen. This Sprite is later moved onto the screen, where it hangs out until it is clicked.

    """
    ## Images here are commandable sprites, so we can tell them what to do using Q below
    print position
    # the image
    img = CommandableImageSprite(screen, OFF_LEFT, image, scale=IMAGE_SCALE)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Set up the updates, etc.

    # A queue of animation operations
    Q = DisplayQueue()

    # Draw a single animation in if you want!
    Q.append(obj=img, action='wait', duration=1.0)
    Q.append(obj=img, action='move', pos=position, duration=0.0)

    # What order do we draw sprites and things in?
    dos = OrderedUpdates(img)  # Draw and update in this order

    start_time = time()

    ## The standard event loop in kelpy -- this loops infinitely to process interactions
    ## and throws events depending on what the user does
    for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):

        if (time() - start_time > MAX_DISPLAY_TIME):
            break

        # If the event is a click:
        if is_click(event):
            break

def run_trial(sequence):

    position = OFF_LEFT
    for value in sequence:
        # look at the image/quadrant we are on currently
        print value
        # we need to turn sequence_value into a number; right now it thinks it's a letter. we are doing something called "casting to an integer"
        value = int(value)
        #choose a random place for the value to go

        #first quadrant
        if value == 0:
            position = quadrant1[random.randint(0,len(quadrant1))-1]

        # second quadrant
        elif value == 1:
            # pick one of the viable positions from quadrant 2
            position = quadrant2[random.randint(0, len(quadrant2))-1]

        #do this for quadrants 3 and 4 also!
        # I got lazy so if it's a 2 or a 3, it's going to spot.d4, but change this!
        else:
            position=spot.d4



        present_trial(target_images[value], position)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# Set up images:
target_images = [kstimulus("feature_cars/car1_blue_stars.png"),
                 kstimulus("feature_cars/car1_red_circles.png"),
                 kstimulus("feature_cars/car1_red_stars.png"),
                 kstimulus("feature_cars/car2_blue_circles.png"),
                 kstimulus("glitch-npcs/regular/npc_salmon.png"),
                 kstimulus("glitch-npcs/regular/npc_jabba.png"),
                 kstimulus("glitch-npcs/regular/npc_myopic_frog.png"),
                 kstimulus("glitch-npcs/regular/npc_piggy.png")]

sequence = "000122221"

run_trial(list(sequence))


