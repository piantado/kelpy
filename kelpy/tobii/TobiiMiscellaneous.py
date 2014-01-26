# -*- coding: utf-8 -*-


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Some miscellaneous useful functions for getting info on a group of TobiiSprites. These functions are designed to be fed a kelpy OrderedUpdate list (as illustrated in the demos, usually named 'dos')
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

