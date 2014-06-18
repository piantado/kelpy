Kelpy Demo2: Display a Few Things, Handle Alternatives

	This demonstration builds on the first demo. It is a slightly more complex demonstration of how to set up an array of images to create multiple CommandableImageSprites. This demonstration uses the DisplayQueue and OrderedUpdates classes to create some simple animations, and later uses the EventHandler to handle clicks on the objects. There are different responses based on whether the CommandableImageSprite is determined to be the 'correct' object or not.

This demo uses the following functions from the Miscellaneous class:
	kelpy_standard_event_loop
		This function loops infinitely to process interactions between the user and the events being displayed onto the screen.
	
	kstimulus
		This function is used to make items in the kelpy/stimulus file available to python/kelpy scripts, reguardless of where the kelpy scripts live on your hard drive.

	filename
		This function, when it is fed a full filepath (such as 'home/mmcgove/Documents/CODE/kelpy/stimuli/image.png') will return the filename (such as 'image.png').

	In addition, this demonstration also uses:
	
	play_sound
		This function is fed the filepath to a signed 16-bit .wav file, and will play the sound.
