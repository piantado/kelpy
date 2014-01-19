Kelpy Demo5: The Blicket Detector (and a simpler drag and drop demo)

	This demonstration shows how to use the DragSprite and DropSprite classes to handle dragging and dropping in your tests. There are a few options of things presented. One of them is a blicket. Drop them onto the detector and to reveal which one!

This demo uses the following functions from the Miscellaneous class:
	kelpy_standard_event_loop
		This function loops infinitely to process interactions between the user and the events being displayed onto the screen.
	
	kstimulus
		This function is used to make items in the kelpy/stimulus file available to python/kelpy scripts, reguardless of where the kelpy scripts live on your hard drive.

	filename
		This function, when it is fed a full filepath (such as 'home/mmcgove/Documents/CODE/kelpy/stimuli/image.png') will return the filename (such as 'image.png').

	play_sound
		This function is fed the filepath to a signed 16-bit .wav file, and will play the sound.

	was_dropped_into_zone
		This function takes an event and it's keyword arguments (**kwargs) as parameters and returns True if one of the dragable objects was dropped into a registered drop zone.

	who_was_dropped
		This function also takes in an event and keyword arguments, but this time it returns the object that was dropped into the drop zone. It is intended to be run in sequence after the previous function has returned true.

	Spots
		This function is fed a screen object, and generates a bunch of useful points for positioning things on the screen. Offscreen positions are labeled according to compass directions, and on screen positions are labeled in groups of 4 across the top, middle, and bottom, numbered left to right. They follow the pattern of spot-object.top1 for the leftmost top onscreen spot. There is also a 'center' spot.

