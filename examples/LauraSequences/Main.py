import os, sys
import pygame
import glob
from random import randint, choice, sample, shuffle
from time import time,sleep
from kelpy.GIFImage import *

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *
import numpy


from kelpy.DragDrop import DragSprite, DropSprite
from kelpy.DragDrop import *


from kelpy.tobii.TobiiSimController import *
from kelpy.tobii.TobiiSprite import *

SCREEN_SIZE_X = 1400
SCREEN_SIZE_Y = 800
IMAGE_SCALE = 0.01
paused = False
exp_start=time()

#to do:
# press key, add sequence again to end of list
# write file
# randomize sequences and insert cover task randomly every 3 to 5
# lookaway for 2 seconds
# glob.glob the stimuli

##############################################
## Set up pygame

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
screen, spot = initialize_kelpy(dimensions=(SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((255,255,255))

OFF_LEFT = (spot.west)

# 4 quadrants, each with possible positions
quadrant0 = [spot.w1,spot.w2, spot.x1,spot.x2]
quadrant1 = [spot.w3,spot.w4, spot.x3, spot.x4]
quadrant2 = [spot.y1,spot.y2, spot.z1, spot.z2]
quadrant3 = [spot.y3,spot.y4, spot.z3, spot.z4]

#######################
#Set up Tobii
use_tobii_sim = True

subject = raw_input('Subject ID: ')
session = raw_input('Session #: ')
session_time = str(time())
if not use_tobii_sim:
	pygame.mouse.set_visible(False)


data_folder = 'data/'
#file_header = ['Subject', 'Session', 'Trial', ...]
#print file_header

#create data folder if it doesn't exist
try:
	os.makedirs(data_folder)
except OSError:
	if not os.path.isdir(data_folder):
		raise
#also append time to filename
data_file = data_folder + subject + '_' + session + '_' + session_time + '.csv'
matched = data_folder + subject+ '_' + session + '_' + session_time + 'matched.csv'

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

blank_box=TobiiSprite(screen, spot.center,kstimulus("laura_diss/window.jpg"),tobii_controller,scale=.5)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def present_trial(chosen_for_sequence,window_positions,images,the_blob):
	#to calculate proportion of looks
	w0,w1,w2,w3=0,0,0,0
	w0_counter = 0
	item_start=time()
	#in order to pause the experiment
	global paused
	if not paused:

		#haven't looked away yet, keep running
		started_lookaway = False

		#if they lookaway for _ seconds
		lookaway_for_time =2.0

		if not use_tobii_sim:
		# start recording the "eye gaze" data
			tobii_controller.start_tracking()

		# A queue of animation operations
		trial_start = time()
		#create the windows as TobiiSprites so they are eye-trackable

		w0 = TobiiSprite(screen, window_positions[0], kstimulus("laura_diss/window.jpg"), scale=.35,tobii_controller=tobii_controller)
		w1 = TobiiSprite(screen, window_positions[1], kstimulus("laura_diss/window.jpg"), scale=.35,tobii_controller=tobii_controller)
		w2 = TobiiSprite(screen, window_positions[2], kstimulus("laura_diss/window.jpg"), scale=.35,tobii_controller=tobii_controller)
		w3 = TobiiSprite(screen, window_positions[3], kstimulus("laura_diss/window.jpg"), scale=.35,tobii_controller=tobii_controller)
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

		images = [
		CommandableImageSprite(screen, OFF_LEFT, images[0], scale=IMAGE_SCALE, name="0"),
		CommandableImageSprite(screen, OFF_LEFT, images[1], scale=IMAGE_SCALE,name="1"),
		CommandableImageSprite(screen, OFF_LEFT, images[2], scale=IMAGE_SCALE,name="2"),
		CommandableImageSprite(screen, OFF_LEFT, images[3], scale=IMAGE_SCALE,name="3")]

		img = CommandableImageSprite(screen, OFF_LEFT,chosen_for_sequence[0][0] , scale=IMAGE_SCALE)

		#create the display Queue and queue up all the images
		Q = DisplayQueue()

		for value in chosen_for_sequence:


			#img = CommandableImageSprite(screen, OFF_LEFT, value[0], scale=IMAGE_SCALE)
			position = value[1]
			#the animation
			Q.append(obj=images[value[2]], action='wait', duration=1.0)
			Q.append(obj=images[value[2]], action='move', pos=position, duration=0.0)
			Q.append(obj=images[value[2]],action='circlescale',duration=1, amount=.08, period=1)
			Q.append(obj=images[value[2]],action='move',pos=OFF_LEFT,duration=0.0)

		dos = OrderedUpdates(the_blob,w0,w1,w2,w3,images)
		# What order do we draw sprites and things in?
		# Draw and update in this order



		for event in kelpy_standard_event_loop(screen,Q, dos, throw_null_events=True):
			#update
			pygame.display.flip()
			#record the active box
			print >> open(matched,'a'),[time()-exp_start,Q.get_obj().get_name()]

			#tobii_controller.record_event(Q.get_obj().get_name())


			#can stop the experiment on a click event
			if is_click(event):
				if not use_tobii_sim:
					tobii_controller.stop_tracking()
					tobii_controller.close_data_file()
					tobii_controller.destroy()
					quit()
				quit()

				if event.type == pygame.QUIT:
					pygame.quit()
					return

			#item animation time has run out, move on
			if time()-item_start >len(chosen_images_and_quadrants)*2:
				break

			#the kind of complicated lookaway stuff
			if not the_blob.is_looked_at():
				if not started_lookaway:
					print "you started looking away"
					#start tracking how long they are looking away for
					started_lookaway_time = time()
					started_lookaway = True
					print time()-started_lookaway_time

				#if they have looked away for longer than lookaway_for_time, it "counts" as a lookaway
				if (time() - started_lookaway_time > lookaway_for_time):
					print "HEY YOURE NOT LOOKING"
					break
			#if they look back at the blob, restart the lookaway clock
			elif the_blob.is_looked_at():
				started_lookaway=False

			if is_space_pressed():
				paused=True




		#can unpause by pressing spacebar
		while paused:
			for event in pygame.event.get():
				if event.type==KEYUP:
					if event.key==K_SPACE:
						paused = False


	else:
		#COVERTASK! (will run when sequence == 5)
		cover_task()


def cover_task():
	######################

	IMAGE_SCALE = 0.4
	screen, spots = initialize_kelpy(dimensions=(1920,1200), bg=(255, 255, 255))
	#game.init()
	#screen = game.display.set_mode([500, 500])
	gameon = True
	background_color = pygame.color.Color("black")

	#while gameon:

	BLICKET_DETECTOR_POSITION = (spots.c1[0], spots.c1[1] + 100)
	blicketd_image_path = (kstimulus("shapes/triangle_yellow.png"))

	BLICKET_DETECTOR_POSITION_2 = (spots.c2[0], spots.c2[1] + 100)
	blicketd_image_path_2 = (kstimulus("shapes/star_pink.png"))

	BLICKET_DETECTOR_POSITION_3 = (spots.c3[0], spots.c3[0], 100)
	blicketd_image_path_3 = (kstimulus("shapes/circle_red.png"))

	pygame.display.flip()  # tells game to refresh the display,
	# all code involving the display of things must go ABOVE this line
	event = pygame.event.poll()  # ask game to examine all things happening in the game now

	# code that responds to keyboard of mouse events goes after pool line
	# need to pool all current events before dealing wtih them
	def present_trial(imagepath):
		thing = DragSprite(screen, spots.cu, imagepath, scale=IMAGE_SCALE)
		blicket_detector = DropSprite(screen, BLICKET_DETECTOR_POSITION, blicketd_image_path, scale=.3)
		blicket_detector_2 = DropSprite(screen, BLICKET_DETECTOR_POSITION_2, blicketd_image_path_2, scale=.3)
		blicket_detector_3 = DropSprite(screen, BLICKET_DETECTOR_POSITION_3, blicketd_image_path_3, scale = .3)
		things = [thing, blicket_detector, blicket_detector_2, blicket_detector_3]
		Q = DisplayQueue()

	# Choose Random Noise
		sounds = ['sounds/Affirmative.wav', 'sounds/Beep.wav', 'sounds/Beep2.wav','sounds/Beep3.wav','sounds/Bing.wav'
				, 'sounds/Button-Reverb.wav','sounds/Button-SP.wav','sounds/Cheek-Pop.wav','sounds/Confirm.wav','sounds/Confirm2.wav',
				'sounds/Confirm3.wav']
		random_sound = random.choice(sounds)
		thing.register_drop_zone(blicket_detector)    # thing.register_drop_zone(blicket_detector_
		dos = OrderedUpdates(*things)  # Draw and update in this order
		for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
			thing.process_dragndrop(event)
			if was_dropped_into_zone(event):
				if who_was_dropped(event) is thing:
					play_sound(kstimulus(random_sound))

			thing.register_drop_zone(blicket_detector_2)
			dis = OrderedUpdates(*things)
			for event in kelpy_standard_event_loop(screen, Q, dis, throw_null_events=True):
				thing.process_dragndrop(event)
				if was_dropped_into_zone(event):
						if who_was_dropped(event) is thing:
							play_sound(kstimulus(random_sound))

				thing.register_drop_zone(blicket_detector_3)
				doo = OrderedUpdates(*things)
				for event in kelpy_standard_event_loop(screen, Q, doo, throw_null_events=True):
					thing.process_dragndrop(event)
					if was_dropped_into_zone(event):
						if who_was_dropped(event) is thing:
							play_sound(kstimulus(random_sound))


	target_images = [kstimulus("shapes/circle_blue.png"), kstimulus("shapes/triangle_green.png"),
					kstimulus("shapes/square_orange.png"), kstimulus("shapes/star_red.png")]
	for i in range(1):
		targetidx = randint(0, 2)
		present_trial(target_images[targetidx])
		print i, targetidx, filename(target_images[targetidx])

	##code will come here when game is over
	while True:
		screen.fill(background_color)
		pygame.display.flip()
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			break
	game.quit()

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

	for i in range(1):

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


# Set up images:


ready = raw_input("Are you ready to begin? Press Enter.")
pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((255,255,255))


#grab the background blobs
blobs = []
for filename in glob.glob('../../kelpy/stimuli/laura_diss/blobs/*'):
	im=filename
	blobs.append(im)

#here is a temp list of sequences
sequences = [ "212302121", "2013210312", "1301203","12301201001", "00112233"]

shuffle(sequences)

#get all the stimuli images
target_images = []
for filename in glob.glob('../../kelpy/stimuli/laura_diss/stimuli/*'):
	im=filename
	target_images.append(im)
shuffle(target_images)

#build a big list (matrix) of allocated images and quadrant positions to each sequence
#put in another file and read in big_list
biglist = []



#allocates all the images to each sequence (and their quadrant positions)
for s in sequences:
	#pick all the images, add them into a list of lists
	shortlist_images = [
		[target_images[0],random.randint(0,len(quadrant0))-1],
		[target_images[1],random.randint(0, len(quadrant1))-1],
		[target_images[2],random.randint(0, len(quadrant2))-1],
		[target_images[3],random.randint(0, len(quadrant3))-1]

		]
	biglist.append(shortlist_images)

	for image in shortlist_images:
	    target_images.remove(image[0])




	#beforehand calculation: each value in sequence and it's quadrant


for s in sequences:


	chosen_blob1 = blobs.pop()
	chosen_blob = TobiiSprite(screen, spot.center, chosen_blob1, tobii_controller, scale=.55)

	the_data = biglist.pop()

	chosen_images_and_quadrants=[]
	for val in s:
		val = int(val)

		if val == 0:
			chosen_images_and_quadrants.append([the_data[0][0],quadrant0[the_data[0][1]],val])
		if val == 1:
			chosen_images_and_quadrants.append([the_data[1][0],quadrant1[the_data[1][1]],val])
		if val == 2:
			chosen_images_and_quadrants.append([the_data[2][0],quadrant2[the_data[2][1]],val])
		if val == 3:
			chosen_images_and_quadrants.append([the_data[3][0],quadrant3[the_data[3][1]],val])


	window_positions = [quadrant0[the_data[0][1]],quadrant1[the_data[1][1]],quadrant2[the_data[2][1]],quadrant3[the_data[3][1]]]
	images = [the_data[0][0],the_data[1][0],the_data[2][0],the_data[3][0]]



	#present the trial! Yay!
	#present the trial by grabbing the quadrant positions from the big matrix

	present_trial(chosen_images_and_quadrants,window_positions,images, chosen_blob)

	#when trial is done (either by running out of time, or by lookaway), do attention_getter
	#MAY USE DIFFERENT ATTENTION GETTER BECAUSE BORING
	attention_circle()



#when all done, shut off the eyetracker and quit
if not use_tobii_sim:
	tobii_controller.stop_tracking()
	tobii_controller.close_data_file()
	tobii_controller.destroy()
	quit()

quit()
