import os, sys
import pygame
from random import randint, choice, sample, shuffle
from time import time

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *
from itertools import *
import csv

"""
    This is the 4th demonstration file for the Kelpy library.
    It demonstrates a boolean concept learning experiment written with python using the Kelpy library, as well as the python csv reader.

    This task presents the subject with stimuli that have two characteristics: a shape and a color.
    The subject selects either "yes" or "no", and is tasked with guessing the rules that govern whether their answer is correct.
    Unbeknownst to the subject, a secret rule has been set in place that selects the 'correct' stimuli.

    In this experiment, the rule is written flexibly, and can easily be changed. This is accomplished by creating a Stimuli class that accepts keyword arguments.
    These arguments are assigned to the stimuli and can be read as attributes of the Stimuli object.
    This allows us to then create a rule using a lambda function. This is just another kind of function that returns true or false depending on some rules we set when creating the function.
    The rule we end up creating in this demo is to return true: if the shape of the object is a star OR if the object is green.

    We display a bunch of colored stars, and a bunch of colored circles. All of the stars are correct, and the green circle is also considered correct.


"""
###################################
## First we set up our screen.
screen = initialize_kelpy( dimensions=(800,600) )

##################
##Generate some spots to place things using the Spots()

spot = Spots(screen)

#################
## and then set up some constants for our images, their scale and where they will be placed
##
WOFFSET = 200
HOFFSET = 100
IMAGE_SCALE = 0.75
OFF_SCREEN = spot.northwest
ON_SCREEN = spot.center

##################
## Followed by some constants for our buttons, their placement on screen, their images, and their scale.
YES_BUTTON_SPOT = spot.bottomq1
NO_BUTTON_SPOT = spot.bottomq4
YES_BUTTON = kstimulus('yes_no_buttons/yes1.png')
NO_BUTTON = kstimulus('yes_no_buttons/no1.png')
BUTTON_SCALE = 0.3


"""
	In this task we give our user a series of items and allow them to learn the correct one.
	The demonstration of correct can be multiple things, and depends on what the user loads into a csv file currently.
	This may change to something more intellegent soon.
"""	
images = []


def show_demo(stimuli):
	"""
		This function demonstrates an object without yes or no buttons for a few seconds
	"""
	demo_time = time()
	MAX_DISPLAY_TIME = 4.0
	
	## We create our image sprite here, inputting the screen to diplay on, it's starting position, the image to use, and the desired scale.
	image = CommandableImageSprite( screen, OFF_SCREEN, stimuli.image, scale=IMAGE_SCALE)
	
	## we then create a display queue, which is what we will use to update things.
	Q = DisplayQueue()
	## also our list of 'things'. This list is used to tell the event_loop what to look at, to track what is clicked and what needs to move, etc.
	## in this case we only have one thing to track. The function still requires a list.
	things = [image]
	
	##this next line adds a new action to the DisplayQueue, we tell it to move the image onto the on screen position over a duration of 1.5 seconds.
	Q.append(obj=image, action='move', pos= ON_SCREEN, duration=1.5)
	## note it will then remain there until the trial ends, or until we were to move it again. In this case, it just hangs out until the trial ends.
	dos = OrderedUpdates(*things)
	
	## we then play a sound to let the subject know whether this object has the desired qualities we are looking for.
	## the rest of the trial plays some similar sounds, to give the subject a hint of whether they have picked correctly or incorrectly.
	if the_rule(stimuli):
		play_sound( kstimulus('sounds/Tada.wav') )
	else:
		play_sound( kstimulus('sounds/Bad_Pick.wav') )
	
	## this is the event_loop for this presentation. Nothing fancy here, when the maximum time is up, end the presentation.
	for event in kelpy_standard_event_loop(screen, Q, dos):
		if (time() - demo_time) >= MAX_DISPLAY_TIME:
			break
			

#####
## Here we create a Stimuli class for use in this experiment.
## 
class Stimuli():
	"""
        This initialization line accepts a filepath (of the stimuli image) and some keyword arguments.
        as it is written, it can accept any keywords, and will assign attributes based on those keywords.
    """
	def __init__(self, input_file, **kwargs):
		self.__dict__.update(kwargs)
		## Then we take the filepath and assign it to our object.image attribute. We will access this later.
		self.image = input_file

def color_shape(input_filepath):
	"""
	This function will take a filepath from the shapes stimuli folder and return it's color and shape.
	Since the filenames are of the format star_purple.png, we will just split out those words from the rest of the filepath.
	"""
	color = input_filepath.rsplit('/')[1].rsplit('_')[1].rsplit('.')[0]
	shape = input_filepath.rsplit('/')[1].rsplit('_')[0]
	return color, shape
	
def load_csv(filename, array_to_load):
	"""
	this function loads a csv file of filepaths and creates an array of Stimuli objects..
	
	It accepts a filename (of the desired .csv file, to be placed in the same directory as the script.)
	as well as an array to load the stimuli into. The stimuli in this case are kept in the /kelpy/stimuli folder, so we use the kstimulus() function to load them.
	
	"""
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
				for element in row:
					its_color, its_shape = color_shape(element)
					new_stimuli = Stimuli(kstimulus(element), color=its_color, shape=its_shape)
					array_to_load.append(new_stimuli)


					
def load_via_itertool(array_to_load):
	""" 
		this function will load shape/color stimuli using the itertools library.
	"""
	colors = ['red', 'green', 'blue', 'pink', 'purple', 'orange', 'yellow' ]
	shapes = ['star', 'circle']
	all_combinations = colors + shapes
	all_combs = permutations(all_combinations, 2)
	for i in all_combs:
		if i[0] in shapes:
			if i[1] in colors:
				print 'loading...' + i[0], i[1]
				loadme = 'shapes/' + i[0] + '_' + i[1] + '.png'
				new_stimuli = Stimuli(kstimulus(loadme), color = i[1], shape=i[0])
				array_to_load.append(new_stimuli)

######################################
## We then create the rule that we will use to determine whether a Stimuli object is 'correct' or not.
## If it's shape attribute is star, *or* if it's color attribute is green, then this function will return true.
the_rule = lambda x: x.shape=='star' or x.color=='green'

def present_trial(stimuli):
	"""
		This is the main function we use to run the trial. It is run twice, once for the 'correct' option, once for the 'incorrect' option.
		It lacks the ability to get shuffled around, so while the many correct and incorrect options are shuffled, they only appear in the order of 'correct' then 'incorrect'.
		There are three sprites on screen, the image, the 'yes' button, and the 'no' button.
		
	"""
	start_time = time()

	Q = DisplayQueue()	
	image = CommandableImageSprite( screen, OFF_SCREEN, stimuli.image, scale=IMAGE_SCALE)
	yes_button = CommandableImageSprite( screen, YES_BUTTON_SPOT, YES_BUTTON, scale=BUTTON_SCALE )
	no_button = CommandableImageSprite( screen, NO_BUTTON_SPOT, NO_BUTTON, scale=BUTTON_SCALE )
	
	things = (image, yes_button, no_button)
	dos = OrderedUpdates(*things)
	## The image is moved on screen...
	Q.append(obj=image, action='move', pos= ON_SCREEN, duration=1.5)
	
	for event in kelpy_standard_event_loop(screen, Q, dos):
		## If it is clicked, we determine whether it is a correct or incorrect image, and whether yes or no was clicked...
		if is_click(event):
			who = who_was_clicked(dos)
			## note the time...
			trial_time = time() - start_time
			## print a bunch of things that we want to track...
			print trial_time, filename(stimuli.image), the_rule(stimuli), stimuli.shape, stimuli.color
			if who is yes_button and the_rule(stimuli):
				## and play an appropriate 'hooray!' or "nope! try again!!" noise.
				play_sound( kstimulus('sounds/Tada.wav'), wait=True)
				break
				
			elif who is no_button and not the_rule(stimuli):
				play_sound( kstimulus('sounds/TadaWah2.wav'), wait=True)
				break
				
			elif who is no_button and the_rule(stimuli):
				play_sound( kstimulus('sounds/Bad_Pick.wav'), wait=True)
				break
				
			elif who is yes_button and not the_rule(stimuli):
				play_sound( kstimulus('sounds/Bad_Pick.wav'), wait=True)
				break


### There are two options for loading your stimuli in this demo, one is via a images.csv file. The way this is written, it will simply intake all the items in the list and determine whether they fit the rule by their filename.

# load_csv('images.csv', images)  ### Use this line to load via the csv file reader, rather than via itertools.

### The other option is to use the load_via_itertool function to generate a list of all the possible combinations.
## It's important to note that this is note actually generating the sprites, just selecting the ones to load since the filenames follow a simple format.
load_via_itertool(images)

## now that all that is set up, we simply run the trial.
## it will run 25 times, with a demonstration of the rule running 5 times throughout.
for x in range(5):
	shuffle(images)	
	show_demo( images[0] ) 
	shuffle(images)	
	for i in xrange(5):
		start_time = time()
		present_trial( images[i] )