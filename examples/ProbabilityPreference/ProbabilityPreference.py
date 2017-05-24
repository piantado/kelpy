''' Welcome to our game! We have two toy boxes. The boxes open every few seconds, and sometimes there is a toy inside. Sometimes there is just a toy in the right box, just in the left box, both boxes, or no boxes. Let's take a look!
Additionally: We have TRIALS and BOX_OPENS. A Trial is when a tuple of probabilities has been assigned to the boxes. A Box_Open is when the box opens during a Trial (this may happen about 5 times).

'''



import os, sys
import pygame
from random import randint, sample, shuffle

from time import time
from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *
import itertools
from random import shuffle
from kelpy.AttentionGetter import *
from kelpy.tobii.TobiiSimController import *
from kelpy.tobii.TobiiSprite import *
import csv


IMAGE_SCALE = .8
BOX_SCALE = 1
#trial time
MAX_DISPLAY_TIME =5

use_tobii_sim = True #toggles between using the tobii simulator or the actual tobii controller
subject = raw_input('Subject ID: ')
session = raw_input('Session #: ')
session_time = str(time())


#also append time to filename
data_folder = 'data/'
file_header = ['Subject', 'Session', 'Trial', 'Trial_Iteration', 'Trial_Start','Trial_End', 'Left_Object', 'Left_Probability','Left_Show', 'LeftBox_Look', 'LeftObj_Look', 'LeftLid_Look', 'Right_Object' ,'Right_Probability', 'Right_Show', 'RightBox_Look', 'RightObj_Look', 'RightLid_Look']
print file_header
#create data folder if it doesn't exist
try:
    os.makedirs(data_folder)
except OSError:
    if not os.path.isdir(data_folder):
        raise

data_file = data_folder + subject + '_' + session + '_' + session_time + '.csv'
##############################################
## Set up eye tracker

##############################################
## Set up pygame

screen, spot = initialize_kelpy(dimensions=(1920,1200))
if use_tobii_sim:
	#create a tobii simulator
	tobii_controller = TobiiSimController(screen)

else:
	#create an actual tobii controller
	tobii_controller = TobiiController(screen)

	# code for when it's actually hooked up to the eye tracker
	tobii_controller.wait_for_find_eyetracker(3)

	#store tobii data in this file
	tobii_controller.set_data_file(data_folder + subject + '_' + session + '_' + session_time + '.tsv')

	#activate the first tobii eyetracker that was found
	tobii_controller.activate(tobii_controller.eyetrackers.keys()[0])



OFF_SOUTH = (spot.south)
LID_SPOT1 = (((screen.get_width()/5) * 1)+20, (screen.get_height()/5)*3 )
LID_SPOT2 = (((screen.get_width()/5) * 4)+20, (screen.get_height()/5)*3 )
left_lid_MOVE = (((screen.get_width()/5) * 1)+20, ((screen.get_height()/6)-50)*3 )
right_lid_MOVE = (((screen.get_width()/5) * 4)+20, ((screen.get_height()/6)-50)*3 )


def present_trial(objects, probabilities, trial,i, writer):
    start_time = time()
    in_right = False
    in_left = False
    left_box =  TobiiSprite( screen, spot.c1, kstimulus("misc/box.png"), tobii_controller, scale=BOX_SCALE)
    left_boxfront = TobiiSprite(screen, spot.c1, kstimulus("misc/boxfront.png"), tobii_controller,scale=BOX_SCALE)
    left_lid =  TobiiSprite( screen, LID_SPOT1, kstimulus("misc/lid.png"), tobii_controller,scale=BOX_SCALE)
    right_box = TobiiSprite(screen, spot.c4, kstimulus("misc/box.png"),tobii_controller, scale=BOX_SCALE)
    right_boxfront = TobiiSprite(screen, spot.c4, kstimulus("misc/boxfront.png"), tobii_controller,scale=BOX_SCALE)
    right_lid = TobiiSprite(screen, LID_SPOT2, kstimulus("misc/lid.png"),tobii_controller, scale=BOX_SCALE)
    left_object = TobiiSprite( screen, spot.c1, objects[0],tobii_controller, scale=IMAGE_SCALE)
    right_object = TobiiSprite(screen, spot.c4, objects[1],tobii_controller, scale=IMAGE_SCALE)


    #the boxes keep opening every when_open seconds, and object appearance is stochastic

    # A queue of animation operations
    Q = DisplayQueue()

    Q.append(obj=left_lid, action='wait', duration=1)
    Q.append(obj=right_lid, action='wait', duration=1)
    Q.append_simultaneous(obj=left_lid, action = 'move', pos=left_lid_MOVE, duration=0.25)
    Q.append_simultaneous(obj=right_lid, action='move', pos=right_lid_MOVE, duration=0.25)

    #with certain probability, reveal object:
    flip1 = random.random()
    if  flip1 < probabilities[0]:
        Q.append_simultaneous(obj=left_object, action='move', pos=spot.b1, duration=.5)
        in_left = True

    #with other probability, reveal object
    flip2 = random.random()
    
    if flip2 < probabilities[1]:
        Q.append_simultaneous(obj=right_object, action='move', pos=spot.b4, duration=.5)
        in_right = True

    Q.append(obj=left_object, action='wait', duration=.25)
    Q.append(obj=right_object, action='wait', duration=.25)

    Q.append(obj=left_lid, action='wait', duration=.25)
    Q.append(obj=right_lid, action='wait', duration=.25)

    Q.append_simultaneous(obj=left_object, action='move', pos=spot.c1, duration=.5)
    Q.append_simultaneous(obj=right_object, action='move', pos=spot.c4, duration=.5)
    Q.append_simultaneous(obj=left_lid, action='move', pos=LID_SPOT1,duration=.5)
    Q.append_simultaneous(obj=right_lid, action='move', pos=LID_SPOT2, duration=.5)

    Q.append(obj=left_object, action='move', pos=OFF_SOUTH, duration=0.0)
    Q.append(obj=right_object, action='move', pos=OFF_SOUTH, duration=0.0)

    # What order do we draw sprites and things in?
    dos = OrderedUpdates([left_box,left_object,left_boxfront, right_box,right_object,right_boxfront,left_lid,right_lid])  # Draw and update in this order

    #main ticker loop
    for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
    # output trial info to csv

        writer.writerow([subject, session, trial, i, start_time, time(), objects[0], probabilities[0], in_left, left_box.is_looked_at(), left_object.is_looked_at(), left_lid.is_looked_at(), objects[1],probabilities[1], in_right, right_box.is_looked_at(), right_object.is_looked_at(), right_lid.is_looked_at()])
        print file_header
        #print subject, session, trial, i, start_time, time(), objects[0], probabilities[0], in_left, left_box.is_looked_at(), left_object.is_looked_at(), left_lid.is_looked_at(), objects[1],probabilities[1], in_right, right_box.is_looked_at(), right_object.is_looked_at(), right_lid.is_looked_at()
        if (time() - start_time > MAX_DISPLAY_TIME):
            break

        # If the event is a click:
        #if is_click(event):
         #   break
		
    # need to do a check for exiting here
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("escaping now")
                quit()
                # make sure to close the data file when exiting, otherwise it'll hang
                if not use_tobii_sim:
                    tobii_controller.stop_tracking()
                    tobii_controller.close_data_file()
                    tobii_controller.destroy()
                    
    
def run_whole_trial(cond, objects,WHEN_OPEN, trial_num, i, writer,images):
	print ">>> Box 1 contains object with "+ str(cond[0])
	print ">>> Box 2 contains object with " + str(cond[1]) +"\n"

	#choose random stimuli
	random_stim = random.sample(objects,2)

	#TODO: calculate how many times to run the box_open
	for i in range(WHEN_OPEN):

		present_trial(random_stim, cond, trial_num,i, writer)
		
	
	#distractor
	#gif_attention_getter(screen, spot.center, images)
	attention_circle()
	print("Hey lovely experimenter! Press Enter to continue once the baby is paying attention!")
	for event in kelpy_standard_event_loop(screen,throw_null_events=True):

		if event.type == KEYDOWN:
			if event.key == K_RETURN or event.key == K_KP_ENTER:
				if not use_tobii_sim:				
						#stop collecting "eye gaze" data
						tobii_controller.stop_tracking()

				#clear_screen(screen) #function defined in Miscellaneous
				return True
	
			#need to do a check for exiting here
			elif event.key == K_ESCAPE:
				#make sure to close the data file when exiting, otherwise it'll hang
				if not use_tobii_sim:
					tobii_controller.stop_tracking()
					tobii_controller.close_data_file()
					tobii_controller.destroy()
	
	# new condition starts
	TRIAL+=1
	
def attention_circle():
	purple = (190,41,236)
	cyan = (0,255,255)
	lime = (50,205,50)
	pink = (255,105,180)
	orange = (255,165,0)
	yellow = (255,215,0)
	
	colors = [purple, cyan, lime, pink, orange, yellow]
	clear_screen(screen)
	radius=20
	color_choice = random.choice(colors)
	pygame.draw.circle(screen,color_choice,spot.center, radius)
	for i in range(3):
		for j in range(70):
			radius=j
			pygame.draw.circle(screen,color_choice,spot.center, radius)
			pygame.display.update()
		pygame.display.update()
		for k in range(70,-1,-1):
			#draw over previous circle in white
			pygame.draw.circle(screen,(250,250,250),spot.center, radius)
			radius=k
			pygame.draw.circle(screen,color_choice,spot.center, radius)
			pygame.display.update()
			
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def experiment():
	
	
    probs = [0.1, 0.25, 0.5, 0.75, 0.9]
    objects = [
            kstimulus("misc/tennis.png") ,
            kstimulus("misc/teddy.png"),
            kstimulus("misc/bug.png"),
            kstimulus("misc/duck.png"),
            kstimulus("misc/firetruck.png"),
            kstimulus("misc/robot.png"),
            kstimulus("misc/gears.png")
            ]

    WHEN_OPEN = 1
    TRIAL = 0
    
    ready = raw_input("Are you ready to begin? Press Enter.")
    pygame.display.set_mode((1920,1200),pygame.FULLSCREEN)
    # hide mouse pointer
    pygame.mouse.set_visible(False)
    
    # open and start writing to data file
    with open(data_file, 'wb') as df:

        # create csv writer (using tabs as the delimiter; the "tsv" extension is being used for the tobii output)
        writer = csv.writer(df, delimiter='\t')
        # write the header for the file
        writer.writerow(file_header)



        condition_set = set()
        for i in itertools.combinations(probs,2):
            condition_set.add(i)
            condition_set.add(i[::-1])
        conditions = list(condition_set)
        shuffle(conditions)

        images = [ kstimulus('/gifs/191px-Seven_segment_display-animated.gif'), kstimulus('gifs/Laurel_&_Hardy_dancing.gif'), kstimulus('gifs/240px-Phenakistoscope_3g07690b.gif') ]
        
        
        for trial_num,cond in enumerate(conditions):
			run=run_whole_trial(cond, objects,WHEN_OPEN, trial_num, i, writer,images)
			
		if not use_tobii_sim:
		#when using the real tobii, make sure to close the eye tracking file and close connection
		tobii_controller.close_data_file()
		tobii_controller.destroy()
			
			
                    
experiment()

			
