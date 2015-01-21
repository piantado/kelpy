.. _stimulus-types:

Stimulus Types
================

There are several different kinds of stimuli in kelpy. Here is an overview of the types:

Sprites
------------

Sprites are an image that can be manipulated either by the code and/or the user, depending on the type of sprite. Each type of sprite has its own set of actions which are executed using the ``DisplayQueue``'s ``append()``. All sprites extend the parent class ``CommandableSprite``, which has a basic set of actions inherited by all other sprites:

CommandableSprite actions:

* **move** - Moves the sprite linearly from its current location to the specified location in a given amount of time.

	Properties:

	* *duration* - Seconds to take until at the new position. Default is 0 (so movement is instantaneous).
	* *pos* - A tuple containing the (x,y) coordinates of the new position

* **wait** - Simply waits in the current position.

	Properties:

	* *duration* - Seconds to wait. If no other command action is given afterwards, the sprite will continue to wait indefinitely. Default is 0.

* **hide** - Immediately hides the sprite.

	Properties:

	* *duration* - Seconds to wait. This does not specifically control how long the sprite is hidden until it appears again. In order to make the sprite visible again, use the command ``show``.

* **show** - Immediately shows the sprite if it is not already visible.
	
	Properties:

	* *duration* - Seconds to wait. This does not specifically control how long the sprite is visible until it is hidden. In order to stop drawing the sprite, use the command ``hide``.


CommandableImageSprite
~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Requires module ``kelpy.CommandableImageSprite``

A ``CommandableImageSprite`` displays an image that can be manipulated by translation, rotation, and scaling.

.. code-block:: python

	sprite = CommandableImageSprite(screen, init_position, imagepath, rotation=0, scale=1.0, brightness=1.0)

Arguments:

* screen
	A reference to the kelpy screen object.

* init_position
	A tuple that contains the (x,y) coordinates for the initial position of the sprite.

* imagepath
	The filepath of the image to be displayed.

* rotation
	The value of the initial rotation of the sprite. Default is 0.

* scale
	The scale of the image to be used, from 0 to 1 (or beyond to enlarge, beware pixelation!). Default is 1.

* brightness
	Initial brightness of the image. Default is 1.

Returns:

* sprite
	A reference to the created ``CommandableImageSprite`` object

CommandableImageSprite actions
################################

	*(Inherits all actions from ``CommandableSprite``, plus...)*

* **waggle** - Jiggles the image for a given amount of time. The animation looks like a swing upwards to the right and then back down to its original position.

	Properties:

	* *duration* - The duration of the waggle motion in seconds.
	* *amount* - The amount of rotation ( units: ???).
	* *period* - A number from 0-1 that indicates the proportion of the duration that is the length of a cycle (where a cycle is rotating counterclockwise for the given amount and then back to the original position). For example, if the period is 1, then it will go through one cycle; if 0.5, then it will go through 2 cycles. Note: the image will automatically go back to its original position after the duration time has passed (resulting in jerky motion if there are not whole cycles).

* **wagglemove** - A ``waggle`` action in combination with a ``move`` action

	Properties:

	* *duration* - The duration of the waggle-move motion in seconds.
	* *amount* - The amount of rotation ( units: ???).
	* *period* - The length of a cycle in seconds (where a cycle is rotating counterclockwise for the given amount and then back to the original position). Note: if the duration is not a multiple of the period, the image will automatically go back to its original position after the duration time has passed (resulting in jerky motion).
	* *pos* - A tuple containing the (x,y) coordinates of the new position for the sprite.

* **wiggle** - A modification of the ``waggle`` action. This motion is oscillatory (moves to the right and then to the left past the original position, like a pendulum). 

	Properties:

	* *duration* - The duration of the wiggle motion in seconds.
	* *amount* - The maximum amount of rotation in degrees (i.e., the amplitude).
	* *cycles* - The number of cycles completed in the given duration. Can also use half cycles. Like the waggle action, the sprite will always end at its original position.

* **circlescale** - This grows and shrinks the sprite repeatedly for a given duration.

	Properties:

	* *duration* - The duration of the circlescale animation.
	* *amount* - The amount of the scaling (units: ???)
	* *period* - A number from 0-1 that indicates the proportion of the duration that is the length of a cycle (where a cycle is growing and then shrinking back to its original size). For example, if the period is 1, then it will go through one cycle; if 0.5, then it will go through 2 cycles. Note: the image will automatically go back to its original size after the duration time has passed (resulting in jerky motion if there are not whole cycles).

* **scale** - This scales the image by the given number over an optionally specified time.

	Properties:

	* *duration* - The time it takes to scale the image, in seconds.
	* *amount* - The amount to scale the image. For example, 0.5 shrinks the image to half its size; 2 would double its size.

* **swap** - Swaps the current image for a different image.

	Properties:

	* *image* - The filepath for the new image.
	* *rotation* - The initial rotation of the new image.
	* *scale* - The initial scale of the new image.

* **rotate** - Rotates the image.

	Properties:

	* *amount* - The degrees of rotation.
	* *duration* - The time it takes to rotate the image for the given amount.

* **darken** - Fades the color of the image.

	Properties:

	* *amount* - A number between 0-1 to indicate how faded the image should be (0 makes the image disappear).
	* *duration* - The time it takes to fade the image, in seconds.

* **swapblink** - Swap between two images repeatedly.

	Properties:

	* *duration* - The duration of the swapping animation in seconds.
	* *period* - The duration an image is displayed on the screen before it is swapped in seconds.
	* *image* - The filepath for the new image.
	* *rotation* - The rotation value of the new image in degrees.
	* *scale* - The scale value of the new image.
	* *brightness* - The brightness value of the new image.

* **restore** - Return the sprite to the original image it was created with.

	*(No properties necessary)*



DragSprite
~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Requires module ``kelpy.DragDrop``

``DragSprite`` is a subtype of ``CommandableImageSprite``. It can be dragged by the user when it is clicked/touched. It is created with the same arguments as a ``CommandableImageSprite`` and also inherits the same command actions. In order to use a ``DragSprite``, you must also call ``process_dragndrop()`` in your kelpy event loop:

.. code-block:: python

	# create the DragSprite
	draggy = DragSprite(screen, init_position, imagepath)

	# add the sprite to an OrderedUpdates object
	dos = OrderedUpdates(draggy)

	# make the DisplayQueue (no need to add any actions)
	Q = DisplayQueue()

	# run the kelpy event loop
	for event in kelpy_standard_event_loop(screen, Q, dos):
		#check for any drag events and update the sprite's position
		draggy.process_dragndrop(event)

When using other sprites with a ``DragSprite``, it is useful to employ ``bring_clicked_to_top()``. This ensures the currently dragged sprite will be drawn on top of other sprites.

.. code-block:: python

	draggy1 = DragSprite(screen, init_position[0], imagepath[0])
	draggy2 = DragSprite(screen, init_position[1], imagepath[1])
	draggy3 = DragSprite(screen, init_position[2], imagepath[2])

	# create a list of the sprites for easy reference later
	sprites = [draggy1, draggy2, draggy3]
	dos = OrderedUpdates(sprites)
	Q = DisplayQueue()

	for event in kelpy_standard_event_loop(screen, Q, dos):
		# use reversed() in order to get the sprite on top 
		# (objects first in the array are drawn first, 
		# and thus under the other objects)
		for sprite in reversed(sprites):
			if sprite.process_dragndrop(event):
				bring_clicked_to_top(sprite, sprites, dos)
				break


DropSprite
~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Requires module ``kelpy.DragDrop``

``DropSprite`` is also a subtype of ``CommandableImageSprite`` and should be used in conjunction with ``DragSprite``. They can detect when ``DragSprites`` are dropped on top of them.

Like a ``DragSprite``, a ``DropSprite`` is created with the same arguments as a ``CommandableImageSprite``. To use ``DropSprites``, you must also call ``register_drop_zone()`` for your ``DragSprites`` in addition to ``was_dropped_into_zone()`` in the kelpy event loop. Check which sprite is on a DropSprite with ``who_was_dropped()``.

.. code-block:: python

	draggy1 = DragSprite(screen, init_position[0], imagepath[0])
	draggy2 = DragSprite(screen, init_position[1], imagepath[1])
	drop_zone = DropSprite(screen, init_position[2], imagepath[2])

	# register drop zone for the DragSprites
	draggy1.register_drop_zone(drop_zone)
	draggy2.register_drop_zone(drop_zone)

	sprites = [draggy1, draggy2, drop_zone]
	dos = OrderedUpdates(sprites)
	Q = DisplayQueue()

	for event in kelpy_standard_event_loop(screen, Q, dos):
		for sprite in reversed(sprites):
			if sprite.process_dragndrop(event):
				bring_clicked_to_top(sprite, sprites, dos)
				break

		# check if a sprite was dropped into a registered drop zone
		if was_dropped_into_zone(event):
			# optionally can check who was dropped
			who = who_was_dropped(event)
			if who is draggy1:
				# do something
			else:
				# do something else

TextSprite
~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Requires module ``kelpy.TextSprite``

``TextSprite`` is for displaying text in the kelpy screen. It only inherits actions from ``CommandableSprite``.

.. code-block:: python

	text = TextSprite(text, screen, init_position)

Arguments:

	* text
		The string of text to be displayed.

	* screen
		A reference to the kelpy screen object.

	* init_position
		A tuple that contains the (x,y) coordinates for the initial position of the text (the text is automatically centered at this point).



Other Visuals
----------------

AttentionGetter
~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Requires module ``kelpy.AttentionGetter``

An ``AttentionGetter`` displays an animated .gif image and optionally plays sound simultaneously. This is particularly useful when running infant studies in order to get the participant's attention back to the screen. Unlike the kelpy sprites, ``AttentionGetters`` are not manipulated within the kelpy event loop.

.. code-block:: python

	#just call the function and you're done!
	gif_attention_getter(screen, position, images, sounds=None, keypress=None, stop_music=True, background_color=(255,255,255), duration=4.0)

Arguments:

	* screen
		A reference to the kelpy screen object.

	* position
		A tuple that contains the (x,y) coordinates for the initial position of the text (the text is automatically centered at this point).

	* images
		Can either be one .gif image filepath or a list of .gif image filepaths to use for the attention getter. If it is a list, the .gif used is selected randomly.

	* sounds
		Can either be one sound filepath or a list of sound filepaths. If it is a list, then the sound used is selected randomly. Default is no sound.

	* keypress
		A pygame keypress code that triggers the attention getter to stop and disappear. Default is no keypress reaction. See the list of key code constants:
		http://www.pygame.org/docs/ref/key.html

	* stop_music
		If True, the music stops after the .gif is played. Otherwise if False, the music continues to play even after the .gif ends. Default is True.

	* background_color
		RGB color of the background that the .gif is displayed on. Default is white.

	* duration
		The duration in seconds the .gif plays for (unless there is a keypress which stops it earlier). Default is 4 seconds.


Sounds
----------------

.. note:: No additional kelpy module required.


Sounds are simply played using ``play_sound()``:

.. code-block:: python

	play_sound(filepath, wait=False, volume=0.65)

Arguments:

	* filepath
		The filepath for the sound file to be played.

	* wait
		If True, the program will wait until the sound is finished playing before it continues. Default is False.

	* volume
		A number from 0-1 that sets the sound's volume level. Default is 0.65.