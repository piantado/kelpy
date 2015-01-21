Getting Started
================

Kelpy experiments follow a basic structure:

	#. Create the kelpy window via ``initialize_kelpy``.
	#. Load the stimuli (images, sounds) and add images to the ``OrderedUpdates`` list.
	#. Add animations to the ``DisplayQueue``.
	#. Run the ``kelpy_standard_event_loop`` and check for task/user events.

You should always include the following kelpy modules:

	* ``kelpy.OrderedUpdates``
	* ``kelpy.DisplayQueue``
	* ``kelpy.EventHandler``

Key Components
-----------------

initialize_kelpy()
~~~~~~~~~~~~~~~~~~~~~

This sets up the kelpy screen based on the given dimensions and background color. All the stimuli are displayed within this window. For example, this function can be called like so:

.. code-block:: python

	screen, spots = initialize_kelpy( dimensions=(1024,768), bg=(250,250,250) )

Where ``screen`` is the reference to the screen object and ``spots`` is a reference to the ``StandardLocations`` object (see :ref:`standard-locations` ).

Alternatively, you can also set the kelpy screen to fullscreen::

	screen, spots = initialize_kelpy( fullscreen=True, bg=(250,250,250) )



OrderedUpdates
~~~~~~~~~~~~~~~~~~~

OrderedUpdates takes a list of kelpy sprites (e.g., `CommandableImageSprite`) and uses the list order as the order to draw/update the sprites. This order is important when stimuli overlap, such as when needing an occluder to hide an image:

.. code-block:: python

	# create your kelpy sprites
	occluder = CommandableImageSprite(screen, start_position, image_paths[0])
	reward = CommandableImageSprite(screen, start_position, image_paths[1])

	# add sprites to a list
	stimuli = [reward, occluder]

	# store the order that we will draw and update things in this variable 'dos'
	dos = OrderedUpdates(stimuli) 

In this example, ``reward`` is drawn first since it is at [0]. ``occluder`` is then drawn second -- since the two sprites share the same location (``start_position``), ``occluder`` is drawn on top of ``reward``.

For the kelpy screen to recognize this ``OrderedUpdates`` list, the ``dos`` object must be passed to the ``kelpy_standard_event_loop`` (see :ref:`kelpy-standard-event-loop`).


.. _display-queue:

DisplayQueue
~~~~~~~~~~~~~~~~~~~

The DisplayQueue stores the order of stimulus events that will occur during the ``kelpy_standard_event_loop``. Kelpy sprites have certain actions they can perform, such as moving or rotating, which can be executed in the order specified in the DisplayQueue:

.. code-block:: python
	
	# create the DisplayQueue
	Q = DisplayQueue()

	# add the sprite events to the queue:
	# first the occluder moves to the north position off-screen (taking 1.5 seconds)
	Q.append(obj=occluder, action='move', pos=spots.north, duration=1.5)
	# once the occluder is finished, the the reward sprite wiggles for 2 seconds
	Q.append(obj=reward, action='wiggle', duration=2, amount=45, cycles=5)

You can also set actions to occur simultaneously by using ``append_simultaneous()``:

.. code-block:: python
	
	# create the DisplayQueue
	Q = DisplayQueue()

	# have the occluder move while the reward wiggles
	Q.append(obj=occluder, action='move', pos=spots.north, duration=1.5)
	Q.append_simultaneous(obj=reward, action='wiggle', duration=2, amount=45, cycles=5)

Like ``OrderedUpdates``, a ``DisplayQueue`` must be passed to the ``kelpy_standard_event_loop``. For a list of specific actions for the different types of kelpy sprites, see :ref:`stimulus-types`.
		

.. _kelpy-standard-event-loop:

kelpy_standard_event_loop()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With your kelpy screen, ``OrderedUpdates`` object, and ``DisplayQueue`` object, you can now run an event loop:

.. code-block:: python

	# pass your 3 objects to the event loop.
	# the loop will run indefinitely while processing interactions,
	# unless you tell it otherwise within the for loop.
	for event in kelpy_standard_event_loop(screen, Q, dos):
	# in this example, once the reward is clicked, a sound is played
	# and then it breaks out of the event loop
		if is_click(event):
			# check what was clicked
			who = who_was_clicked(dos)
			if who is reward:
				play_sound(sound_file, wait=True, volume=0.7)
				break

Within the for loop, you can detect user events (such as clicking on objects, dragging objects), add additional sprite actions to the ``DisplayQueue``, play sounds, and whatever else necessary for the flow of your experiment. 


Other Useful Classes/Functions
--------------------------------

.. _standard-locations:

StandardLocations
~~~~~~~~~~~~~~~~~~~~

Once a kelpy screen is created, a ``StandardLocations`` object is returned along with a reference to the screen object itself. ``StandardLocations`` has several pre-defined properties that refer to spots both on and off the screen, based on the dimensions of the kelpy window. These spots can be used for image placement. Description of available positions:

**Off-screen locations**
	
	* north
	* northeast
	* east
	* southeast
	* south
	* southwest
	* west
	* northwest

**On-screen locations**

	Default on-screen locations are based on a 4x4 grid pattern, with rows as letters a-d and columns as numbers 1-4. For example, ``a1`` is the top left corner, while ``d1`` is the bottom left corner. There is also a row of 4 positions at the middle height of the screen (``midrow1``, ``midrow2``, etc.) and a column of 4 positions at the middle width  (``midcol1``, ``midcol2``, etc.). The center position of the screen is ``center``.


who_was_clicked()
~~~~~~~~~~~~~~~~~~~~~

During the ``kelpy_standard_event_loop``, if you make a call to ``who_was_clicked()`` and pass your DisplayQueue as an argument, the function will return what kelpy sprite was clicked on, if any.

.. code-block:: python

	who = who_was_clicked(dos)
	if who is correct_sprite:
		#return something positive
	elif who is wrong_sprite:
		#return something negative?
	else:
		#possibly do nothing since no sprite was clicked


kstimulus()
~~~~~~~~~~~~~~~~~~

This function simplifies calling stimuli files that are included with kelpy, located in the ``kelpy/stimuli`` directory. For example, if you wanted to use the ``Beep.wav`` sound file:

.. code-block:: python

	beep = kstimulus('sounds/Beep.wav')
	play_sound(beep)

There are many images and sounds in the stimuli library, so take some time to browse through them!


filename()
~~~~~~~~~~~~~~~~~

As the function name implies, this returns just the filename (e.g., ``image.png``) of the filepath that is passed to it (e.g., ``/home/user/kelpy-master/kelpy/stimuli/image.png``). This is useful when outputting either to the command window or to a data file what stimuli were displayed/played.


Code Reference
-------------------------------
.. autofunction:: kelpy.Miscellaneous.initialize_kelpy
.. autoclass:: kelpy.OrderedUpdates.OrderedUpdates
	:members:
.. autoclass:: kelpy.DisplayQueue.DisplayQueue
	:members:
.. autofunction:: kelpy.Miscellaneous.kelpy_standard_event_loop