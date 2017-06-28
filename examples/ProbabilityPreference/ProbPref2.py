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
from random import shuffle, randint
from kelpy.AttentionGetter import *
from kelpy.tobii.TobiiSimController import *
from kelpy.tobii.TobiiSprite import *
import csv
import glob
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import VideoFileClip

BGCOLOR = (0,0,0)
IMAGE_SCALE = .8
BOX_SCALE = 1
MAX_DISPLAY_TIME =100
TRIAL = 1

BOXES = []
for filename in glob.glob('../../kelpy/stimuli/boximages/*'):
    im=filename
    BOXES.append(im)


OBJECTS = []
for filename in glob.glob('../../kelpy/stimuli/socialstim/*'):
    im=filename
    OBJECTS.append(im)

PROBABILITIES = [0.1, 0.25, 0.5, 0.75, 0.9]

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

screen, spot = initialize_kelpy(dimensions=(1400,900), bg=BGCOLOR)
LOCATION = ((screen.get_width() /2 ), (screen.get_height() /2 )-400)
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

def smiley_baby_distractor():
    clip = VideoFileClip(kstimulus('gifs/babylaugh.mov'))
    clip=clip.resize(height=800,width=1300)
    clip.preview()





#run a single Open Box animation as part of the trial. count these!
def open_box(object, box, probability, trial, writer, BGCOLOR):
    pygame.display.set_mode((1400,900),pygame.FULLSCREEN)
    play_sound(kstimulus('music/hothothot.wav'))
    start_time = time()
    screen.fill(BGCOLOR)
    box =  TobiiSprite( screen, spot.center, box, tobii_controller, scale=BOX_SCALE)
    object = TobiiSprite( screen, spot.south, object,tobii_controller, scale=IMAGE_SCALE)
    blankbox = TobiiSprite( screen, spot.center, '../../kelpy/stimuli/misc/blankbox.png', tobii_controller, scale=BOX_SCALE)

    Q = DisplayQueue()

    Q.append(obj=box, action='wait', duration=1)


    for i in range(100):
        #with certain probability, reveal object:
        flip = random.random()
        #print flip
        if  flip < probability:
            Q.append_simultaneous(obj=object, action='move', pos=spot.center, duration=0)
            present = True
        Q.append(obj=box, action='move', pos=spot.north,duration=1)
        Q.append(obj=box, action='wait',duration=.25)
        Q.append(obj=box, action='move', pos=spot.center,duration=1)
        Q.append(obj=box, action='wait',duration=.25)
        Q.append_simultaneous(obj=object, action='move', pos=spot.north, duration=0)

        #if a baby looks away for 3 seconds, the trial ENDS. How do we deal with this?



    dos = OrderedUpdates([blankbox, object, box ])






    #main ticker loop
    for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
    # output trial info to csv
        pygame.draw.rect(screen,(0,0,0),((screen.get_width() /2 )-200, (screen.get_height() /2 )-200,400,400),4)
        pygame.draw.rect(screen,BGCOLOR,((screen.get_width() /2 )-200, (screen.get_height() /2 )-601,400,400),0)
        pygame.draw.rect(screen,BGCOLOR,((screen.get_width() /2 )-200, (screen.get_height() /2 )+201,400,400),0)
        pygame.display.update()
        #writer.writerow([subject, session, trial, i, start_time, time(), objects[0], probabilities[0], in_left, left_box.is_looked_at(), left_object.is_looked_at(), left_lid.is_looked_at(), objects[1],probabilities[1], in_right, right_box.is_looked_at(), right_object.is_looked_at(), right_lid.is_looked_at()])
        #print file_header
        #print subject, session, trial, i, start_time, time(), objects[0], probabilities[0], in_left, left_box.is_looked_at(), left_object.is_looked_at(), left_lid.is_looked_at(), objects[1],probabilities[1], in_right, right_box.is_looked_at(), right_object.is_looked_at(), right_lid.is_looked_at()
        if (time() - start_time > MAX_DISPLAY_TIME):
            break

        #we want this for about 2 seconds
        if(not(blankbox.is_looked_at())):
            print blankbox.is_looked_at()
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







def run_trial(trial, prob, writer):
    #pick a box
    box = random.choice(BOXES)
    #pick an object
    object = random.choice(OBJECTS)

    BGCOLOR=(randint(0,255),randint(0,255),randint(0,255))
    screen.fill(BGCOLOR)
    pygame.display.update()
    print "The box contains the object with " + str(prob) + " probability."

    open_box(object, box, prob, trial, writer, BGCOLOR)
    smiley_baby_distractor()
    #gif_attention_getter(screen,spot.center,kstimulus("gifs/babylaugh.gif"))
    print("Press Enter to continue once the baby is paying attention!")
    for event in kelpy_standard_event_loop(screen,throw_null_events=True):

        if event.type == KEYDOWN:
            if event.key == K_RETURN or event.key == K_KP_ENTER:
                return True
            if event.key == K_r:
                #replay distractor!
                smiley_baby_distractor()



            #need to do a check for exiting here
            elif event.key == K_ESCAPE:
                #make sure to close the data file when exiting, otherwise it'll hang
                if not use_tobii_sim:
                    tobii_controller.stop_tracking()
                    tobii_controller.close_data_file()
                    tobii_controller.destroy()


def run_all():
    ready = raw_input("Are you ready to begin? Press Enter.")
    pygame.display.set_mode((1400,900),pygame.FULLSCREEN)
    # hide mouse pointer
    pygame.mouse.set_visible(True)

    # open and start writing to data file
    with open(data_file, 'wb') as df:

        # create csv writer (using tabs as the delimiter; the "tsv" extension is being used for the tobii output)
        writer = csv.writer(df, delimiter='\t')
        # write the header for the file
        writer.writerow(file_header)



        condition_set = set()
        for prob in PROBABILITIES:
                #run infinitely (until baby looks away)
                run=run_trial(TRIAL, prob, writer)

run_all()
