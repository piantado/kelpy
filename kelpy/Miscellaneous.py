# -*- coding: utf-8 -*-
"""
	Some miscellaneous useful functions
	
"""
import os
import sys
import random
import pygame
from time import time
from pygame.locals import *
from kelpy.KelpyScreen import *


## Some global variables we care about
screen, clock = [None]*2

OFFSCREEN = [-10000, -10000]

Infinity = float("inf")

tab = '\t'
background_color = (255,255,255)

SPACEBAR_CHANGE_EVENT = pygame.USEREVENT + 0x1 # called by our main loop when space bar changes state (pressed to unpressed, etc)
def is_space_pressed(): return pygame.key.get_pressed()[K_SPACE]
SPACEBAR_NOHOLD_EVENT = pygame.USEREVENT + 0x2 # called by our main loop whenever the spacebar is NOT held down
NULL_EVENT            = pygame.USEREVENT + 0x3
ZONE_EVENT            = pygame.USEREVENT + 0x4
EXIT_KELPY_STANDARD_EVENT_LOOP            = pygame.USEREVENT + 0x5 # this event is for exiting loops, after completing some queue event
KELPY_USER_EVENT      = pygame.USEREVENT + 0x6

#pygame.mixer.pre_init(44100,-16,2, 1024 * 3) # sometimes we get scratchy sound -- use this from http://archives.seul.org/pygame/users/Oct-2003/msg00076.html
def ifelse(x,y,z):
	if x: return y
	else: return z
	
	
def q(x): return "\""+str(x)+"\""

def die(x):
	print  >>sys.stderr, x
	quit()
	
def flip(): return (random.random() < 0.5);

def kstimulus(*args):
	"""
		Returns the stimulus for a path f (relative to the kelpy stimulus file)
	"""
	
	f = os.path.dirname( __file__ )+"/stimuli/"
	
	if len(args) == 1: f = f+args[0]
	else:              
		for a in args:
			#print "A=",a, a[1], a[1] == '.', f[-1] != '/' and a[1] != '.' and a[1] != '/'
			if f[-1] != '/' and a[0] != '.' and a[0] != '/': f = f+"_"+a # don't append when we ar a slash or an extension
			else:            f = f+a
	
	return f

def next_alphabetical(s):
	"""
		Returns the next string in alphabetical order ( "aab" -> "aac", etc)
		From http://stackoverflow.com/questions/932506/how-can-i-get-the-next-string-in-alphanumeric-ordering-in-python
	"""
	strip_zs = s.rstrip('z')
	if strip_zs: return strip_zs[:-1] + chr(ord(strip_zs[-1]) + 1) + 'a' * (len(s) - len(strip_zs))
	else: return 'a' * (len(s) + 1)

	
blankcursor_strings = (               #sized 24x24
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ")
blank_cursor=pygame.cursors.compile(blankcursor_strings, black='X', white='.', xor='o')

def xor(x,y): return (x and (not y)) or ( (not x) and y )

def sample1(*args): return sample_one(*args)
def sample_one(*args): 
	if len(args) == 1: return random.sample(args[0],1)[0] # use the list you were given
	else:             return random.sample(args, 1)[0]   # treat the arguments as a list

def loop_till_key(key=K_RETURN):
	
	while True:
		if pygame.key.get_pressed()[key] == 1: return
		
		for event in pygame.event.get():
				if event.type == QUIT: quit()
				if event.type == KEYDOWN and event.key == K_ESCAPE: quit()


def play_sound(sound, wait=False, volume=0.65):
    """ 
    Simplifies the pygame sound module into a single function for playing sounds.
    
    Set wait to true to tell the program to wait until the sound if finished to continue.
    This may fix problems where the program ends before a sound finishes playing, and makes it seem like the sound
    hasn't started playing at all.
    
    volume sets the volume, between 0.0 and 1.0 
    """
    #snd = pygame.mixer.Sound( sound )
    #snd.set_volume( volume )
    pygame.mixer.music.load(sound)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    if wait:
        while pygame.mixer.music.get_busy(): pass
        


def initialize_kelpy(dimensions=(1024,768), bg=(250,250,250), fullscreen=False):
	"""
		Calls a bunch of pygame functions to set up the screen, etc. 
		- Fullscreen - if true, we override the dimensions.
	"""
	
	global background_color # change the up-one-level variable
	background_color = bg
	
	pygame.init()
	
	if fullscreen: 
		screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode(dimensions)
	clock = pygame.time.Clock()
	
	## And load our icon
	icon = pygame.image.load(kstimulus("icons/icon_100x100.png"))
	pygame.display.set_icon(icon)
	pygame.display.set_caption("Kelpy")
	
	if not pygame.font: print 'Warning, fonts disabled'
	if not pygame.mixer: print 'Warning, sound disabled'
	
	#kelpy_screen = KelpyScreen(screen)
	#return kelpy_screen

	return screen
	
def clear_screen(screen):
	screen.fill(background_color)
	pygame.display.flip()


def kelpy_standard_event_loop(screen, *args, **kwargs):
	"""
		This is a cute way to loop indefinitely (or until max time -- TODO implement this), while updating kelpy objects. 
		Here, each arg gets "update()" called on each loop, and we yeild the current time. 
		We also process the screen flips, etc. etc. 
		
		NOTE: SPACEBAR_CHANGE_EVENT sends the new state, NOT the old state! So if you want the time for lookaways, you have to look at times 
		TODO: WE SHOULD CHANGE THIS AFTER COMPBABY RUNS SO THAT THE is_space_pressed is the OLD time, so its reporting events (instead of new stats with prior times)
		If a pygame event of type LOOP_EXIT_EVENT is thrown, then we exit this loop
	"""
	
	# Make events for when spacebar changes status
	old_is_space_pressed = is_space_pressed
	start_space_up = float("-inf")
	last_space_change_time = float("-inf")
	while True:
		pygame.display.flip() # display the previous cycle
		
		if kwargs.get('throw_spacebar_events', False):
			# handle space press events -- throw changes and throw all holds
			sp = is_space_pressed()
			if old_is_space_pressed != sp:
				t = time()
				pygame.event.post(pygame.event.Event(SPACEBAR_CHANGE_EVENT, is_space_pressed=sp, time_changed=(t-last_space_change_time)))
				old_is_space_pressed = sp
				last_space_change_time = t
				
				if not sp: start_space_up = t # record the time of space press starting
			if not sp: # post the spacebar hold event
				pygame.event.post(pygame.event.Event(SPACEBAR_NOHOLD_EVENT, time=(time()-start_space_up)))
		
		if kwargs.get('throw_null_events', False): # these will throw a "NULL" event every iteration, in order to process things outside this loop each time point
			pygame.event.post(pygame.event.Event(NULL_EVENT))
		
		
		# process all events
		for event in pygame.event.get():
			
			yield event # so we can handle EXIT, etc., outside, but don't have to
			
			if event.type == QUIT: quit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE: quit()
			elif event.type == EXIT_KELPY_STANDARD_EVENT_LOOP: return # we are done with this loop
			
		# fill the background and update everything
		screen.fill(background_color)
		for a in args:
			if isinstance(a, list): 
				for ai in a: ai.update()
			else: a.update() # love you, duck typing XXOO

def filename( inputFilepath ):
	"""
		This function returns the filename when passed a full filepath.
	"""
	return inputFilepath.rsplit('/', 1)[1]

			
class Spots():
	"""
		This class can be used to call offscreen and onscreen spots to position things on a screen.
		It is used by the following code:
		screen = initialize_kelpy( dimensions=(800,600) )  ## INITIALIZE THE SCREEN OBJECT...
		spots = Spots(screen)   ## FEED THE SCREEN OBJECT TO THE SPOTS OBJECT...
		print spots.west	## YOU CAN NOW CALL THE POSITIONS FROM THE OBJECT AS ATTRIBUTES! YAY!
	"""
	def __init__(self, screen):
		self.west = (-screen.get_height(),  screen.get_width() /2 )
		self.northwest = ( -screen.get_height(), -screen.get_width() )
		self.north = ( screen.get_width()/2, -screen.get_height() )
		self.northeast = ( screen.get_width() *2, -screen.get_height() )
		self.east = ( screen.get_width() * 2, screen.get_height()/2 )
		self.southeast= ( screen.get_width() * 2, screen.get_height() * 2 )
		self.south = ( screen.get_width()/2 , screen.get_height() * 2 )
		self.southwest = ( -screen.get_width(), screen.get_height()*2 )
		self.center = (screen.get_width()/2, screen.get_height()/2 ) 
		
		self.topq1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*2 )
		self.topq2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*2 )
		self.topq3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*2)
		self.topq4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*2 )
		
		self.middleq1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*3 )
		self.middleq2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*3 )
		self.middleq3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*3 )
		self.middleq4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*3 )
		
		self.bottomq1 = ((screen.get_width()/5) * 1, (screen.get_height()/5)*4 )
		self.bottomq2 = ((screen.get_width()/5) * 2, (screen.get_height()/5)*4 )
		self.bottomq3 = ((screen.get_width()/5) * 3, (screen.get_height()/5)*4 )
		self.bottomq4 = ((screen.get_width()/5) * 4, (screen.get_height()/5)*4 )

		self.center = ((screen.get_width() /2 ), (screen.get_height() /2 ) )
