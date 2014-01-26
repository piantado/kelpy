# -*- coding: utf-8 -*-

from time import time
from kelpy.Miscellaneous import *

class DisplayQueue:
	"""
		A displayqueue stores a list of objects and actions to call on them. 
		It also stores a list of "child(ren)" display queues that get updated at the same time. This allows it
		to process events simultaneously -- by calling append_simultaneous you create new children.
		      
		This returns True on update() when it's all done.
	"""
		
	# each queue stores a bunch of children queues that are sub-processes that are updated whenever we are
	def __init__(self, obj=None):
		self.obj = obj
		self.commands = []
		self.children = []
		self.first = True
		self.finish = False
		self.snd = None
		pass
	
	def is_empty(self):
		"""
			Return true if we (and all our kids) have no pending operations		
		"""
		return len(self.commands) == 0 and all([c.is_empty() for c in self.children])
		
	def start(self):
		self.start_time = time()
		
	def append(self, **args ):
		"""
			Append a single command onto the queue.
		"""
		self.commands.append( args )
	
	def append_simultaneous(self, **args):
		"""
			# Push on a simultanous command, simultaneous with the command that came before
		"""
		args['simultaneous'] = True
		self.append(**args)
		
	
	def next_action(self):
		"""
			# force movement onto the next action
		"""
		del self.commands[0]
		self.start_time = -1
	
	# clean out the Q
	def purge(self):
		self.commands = []
		self.first = True
		
		# and stop sounds
		if self.snd is not None:
			self.snd.stop()
			self.snd = None
			
		
	def update(self):
		"""
			Update on DisplayQueues returns true when we are done with the queue
			
			This is structured as a tree, so that each DisplayQueue has a bunch of children, which update at the same time.
			This is how we handle simultaneous events
			
			self.update() returns True when we are done running
		"""
		
		# Cute--update the kids and remove ones that retun True
		self.children = [ x for x in self.children if not x.update() ]
		
		# then update myself
		if len(self.commands) > 0:
			
			args = self.commands[0]
			
			# Handle the children!
			# while the *next* command is a simultanous one, push it onto my children
			while len(self.commands) > 1 and self.commands[1].get('simultaneous', False):
				q = DisplayQueue()
				q.append(**self.commands[1])
				self.children.append(q)
				del self.commands[1]
			
			## Here are some things we can process immediately
			## Some specialized functions we can implement here without going into a displayqueue
			if args['obj'] == 'sound': # if this, then we will play a sound file
				if self.first:
					# this declaration of a new sound object will make them overlap if multiples are played
					self.snd = pygame.mixer.Sound( args['file'] )
					self.snd.set_volume( args.get('volume', 0.5) )
					self.snd.play()
					self.start_time = time()
					args['duration'] = self.snd.get_length() # how long is it? This is what determines when it's done
					
					## The rest is handled below
					
				if not args.get('wait', False): self.finish = True # we are done with this command
			
			elif args['obj'] == 'call': # allow calling arbitrary functions
				args['function'].__call__()
				self.finish = True # we are done with this command
			elif args['obj'] == 'block_event': # allow us to queue blocking and allowing events
				pygame.event.set_blocked(args['type'])
				self.finish = True # we are done with this command
			elif args['obj'] == 'allow_event':
				pygame.event.set_allowed(args['type'])
				self.finish = True # we are done with this command
			elif args['obj'] == 'throw_event': # allow queues to throw pygame events
				pygame.event.post(args['event']);
				self.finish = True # we are done with this command
			else:
				###################################################
				## Otherwise, we can update it by the object
				
				# If this is the first loop for this command
				# keep track of the start time
				if self.first: 
					self.start_time = time() # update the time
				
				## Now we define some default variables which are appended (overwritten) and passed as args
				args['first'] = self.first   # Is this the first iteration?
				args['finish'] = self.finish # Is this the last iteration?
				args['start_time'] = self.start_time # pass this as an argument
				args['obj'].update_action(**args) # call update action on the object
				
			# if u returns true or we have run long enough,
			# set the self.finish tag so that next loop around, we will 
			if self.finish:
				del self.commands[0] #we're done with this command
				self.first = True # next loop we start the next command
				self.finish = False # must reset this
			elif (time() -  self.start_time) >= args.get('duration', 0.0): 
				# We must loop one more time to finalize (e.g. allow "finish" to be passed in)
				# so this does not exit--we have one more loop
				self.finish = True
			else:
				self.first = False # reset this
				
		return len(self.children)==0 # we are done if self.commands is empty and all children are done


