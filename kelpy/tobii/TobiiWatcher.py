# -*- coding: utf-8 -*-

from time import time

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	This contain some functions for getting eye tracking data on a group of TobiiSprites. These functions are designed to be fed a kelpy OrderedUpdate list (as illustrated in the demos, usually named 'dos')
#
#	This also contains the class Lookaway that keeps track of lookaway time when used within the kelpy event loop
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def looking_at_what(things):
	"""
	looking_at_what will return the object that is currently being looked at based on current eye gaze data. As long as the tobii eyetracker is tracking, this can be called as such:
	
	thing_looked_at = looking_at_what(dos)
	
	Remembering that 'dos' just refers to the kelpy OrderedUpdate list.	

	Just like who_was_clicked() in kelpy.EventHandler: this function is not designed to handle looking at multiple objects, ie if there are two sprites on top of each other, it will return the first one in the ordered updates list.
	This may mean the item on the bottom will be returned first, if it is in line to be checked first.
	
	"""
	for x in iter(things, ):
		if x.is_looked_at():
			return x
	
	return None
	
def looking_proportions(things, trial_time):
	"""
	Based on the given trial_time, this function will determine the looking time proportionfor each object passed to it. The results are returned as a dictionary with keys as the objects as values as the proportions calculated from the given trial_time

	like looking_at_what(), it is given a kelpy OrderedUpdate list as "things":
	
	trial_time = time() - start_time
	proportion_dict = looking_proportions(dos, trial_time)
	
	"""
	proportions = {}
	for x in iter(things, ):
		proportions[x] = x.get_look_time()/trial_time
		
	return proportions


class Lookaway():

	"""
	Keeps track of lookaway time

	"""

	def __init__(self, tobii_controller):
		self.tobii_controller = tobii_controller

		#initialize variables that need to be tracked over time
		self.current_lookaway_time = 0
		self.last_lookaway_timepoint = -1

	def update_lookaway(self):
		"""
		Call this within the kelpy loop to keep track of lookaway time
		
		"""
		if None in self.tobii_controller.get_center_gaze():
			current_time = time() 
			if (self.last_lookaway_timepoint != -1):
				self.current_lookaway_time = self.current_lookaway_time + (current_time - self.last_lookaway_timepoint) 

			self.last_lookaway_timepoint = current_time
			
		else:
			self.current_lookaway_time = 0
			self.last_lookaway_timepoint = -1

		return self.current_lookaway_time
