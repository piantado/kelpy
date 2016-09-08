# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tobii sim controller for kelpy
#		this controller is intended to be used as a simple development tool to simulate 
#		gaze input from a tobii eye tracker. it returns a tuple of the mouse's position.
#		
#		this version does not simulate a full range of tobii data, like the validity codes or depth or anything fancy.
#
#		
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##this version uses nothing that the original uses.
import pygame
from pygame.locals import *


## This is a tobii simulator made mostly from bandaids and tape.


class TobiiSimController:

	def __init__(self, screen):
		self.screen = screen  
		self.eyetrackers = None
	
	def get_center_gaze( self ):
		# print pygame.mouse.get_pos()
		return (pygame.mouse.get_pos())
	
	def print_mouse_position(self):
		print (integer(pygame.mouse.get_pos()[0]),integer(pygame.mouse.get_pos9[1])) 
		

	def wait_for_find_eyetracker(self, timeout=1000):
	
		pass  
	def on_eyetracker_browser_event(self, event_type, event_name, eyetracker_info):
		pass
        
	def destroy(self):
		pass
        #No need to destroy! There's nothing here!
        
    ############################################################################
    # activation methods
    ############################################################################
	def activate(self,eyetracker):
		print "TobiiSim Activated!"
        
	def on_eyetracker_created(self, error, eyetracker, eyetracker_info):
		pass
                
    ############################################################################
    # calibration methods
    ############################################################################
    
	#none for now since the lab does tobii calibration through TobiiStudio...
   
    ############################################################################
    # tracking & data methods
    ############################################################################
    
	def start_tracking(self):
		self.gazeData = []
 		self.eventData = []
    
	def stop_tracking(self):
		self.flush_data()
		self.gazeData = []
		self.eventData = []
    
	def on_gazedata(self,error,gaze):
		self.gazeData.append(gaze)
    
	def get_gaze_position(self,gaze):
	# """
	# Returns left x,y and right x,y positions in screen coordinates.
	# Since Tobii uses normalized units, need to multiply by screen size. 
	# This assumes that the kelpy window is fullsized; may need to change this for future versions?
		
	# """
 #    	# Verify that the gaze data is valid, otherwise reject it.
 #    	# Summarized from the Tobii SDK Guide:
	# 	# 0 = found both eyes
 #    	# 1 = found one eye, probably the correct eye assignment
 #    	# 2 = found one eye, but not sure which
 #    	# 3 = found one eye, but probably the other eye
 #    	# 4 = found no eyes
 #    	# Should just use data with code 0 or 1 (reject 2+)
            
	# if gaze.LeftValidity >= 2 and gaze.RightValidity >= 2:
	# 	return (None,None,None,None)

 #        return (int(gaze.LeftGazePoint2D.x*self.screen.get_width()),
 #                int(gaze.LeftGazePoint2D.y*self.screen.get_height()),
 #                int(gaze.RightGazePoint2D.x*self.screen.get_width()),
 #                int(gaze.RightGazePoint2D.y*self.screen.get_height()))
		return (pygame.mouse.get_pos())  ## yet another bandaid. this one will not work correctly, though.

    
	def get_current_gaze_position(self):

    
		if len(self.gazeData)==0:
			return (None,None,None,None)
		else:
			return None
 

    # gaze information is simply reporting mouse pointer position
	def get_left_gaze(self):
		return pygame.mouse.get_pos()
		
	def get_right_gaze(self):
		return pygame.mouse.get_pos()
		
	def get_center_gaze(self):
		return pygame.mouse.get_pos()
    

    #pre-existing data writing methods; adjusted slightly for validity codes
	def set_data_file(self,filename):
		pass
        
	def close_data_file(self):
		pass
    
	def record_event(self,event):
		pass
    
	def flush_data(self):
		pass