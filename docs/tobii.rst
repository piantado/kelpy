.. tobii:

Tobii Integration
=====================

Kelpy also supports the use of a Tobii eye tracker in experiments.

.. note:: 
	As listed in the Tobii SDK Developer's Guide, the following Tobii Eye Trackers are supported: **Tobii X60, Tobii X120, Tobii T60, Tobii T120, Tobii T60 XL,
	Tobii TX300, Tobii X1 Light, Tobii X2-30 and Tobii X2-60.**
	Models that are not supported are: **Tobii 1750, Tobii X50, Tobii 2150, Tobii 1740 (D10), Tobii P10, C-Eye,
	PCEye, Tobii IS-1 and Tobii Rex.**

To run an experiment with a Tobii, you will need the ``TobiiController`` module and the ``TobiiSprite`` module. Optionally you can also include the ``TobiiWatcher`` module.

When developing your experiment without an eye tracker hooked up, you can use the ``TobiiSimController``.

To include these modules, use the format::

	import kelpy.tobii.nameOfModule

Check out the tobii examples under the folder ``examples/demo-tobii`` for complete experiment setups.



TobiiController
-------------------

The tobii controller is the interface between kelpy and your Tobii. It controls connecting to your Tobii as well as gathering eye data that is then written to an output file. Here is the basic setup for initializing a Tobii::

	# this creates a TobiiController that calls the Tobii SDK code
	tobii_controller = TobiiController(screen)

	# this searches for the tobii eyetracker that is connected.
	# It times out based on the given amount of seconds (the default is 1,000 seconds) and exits this program
	tobii_controller.wait_for_find_eyetracker(3)

	#set the name of the data file that will output all of the Tobii data
	tobii_controller.set_data_file('testdata.tsv')

	#activate the first tobii eyetracker that was found
	tobii_controller.activate(tobii_controller.eyetrackers.keys()[0])

For each trial, you will then need to start and stop the eye tracker to prevent data collection between trials::

	#start eye tracking; this can be called later in your script once all the experiment setup is completed
	tobii_controller.start_tracking()

	trial_time = 5.0
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		#end the trial once the time is up
		if (time() - start_time > trial_time): 
			break

		#this is set specifically for the tobii controller,
		#otherwise the program hangs since the text file is not closed
		if event.type == QUIT:
			 tobii_controller.close_data_file()
			 tobii_controller.destroy()

		#stop eye tracking when you no longer need the eye data for the trial
		tobii_controller.stop_tracking()

As shown in the sample code above, you may also need to check for any attempts to exit out of the experiment before it is complete; if there are any, make sure you close the data file (using ``tobii_controller.close_data_file()``) and disconnect from the Tobii (using ``tobii_controller.destroy()``) before ending the program. These two function calls should also be included at the end of your script.


TobiiSprite
---------------

A ``TobiiSprite`` is a variation of a ``CommandableImageSprite``. You can pass all the same arguments to a ``TobiiSprite``; the only difference is that you must also pass the TobiiController object as well::

	sprite = TobiiSprite(screen, init_position, imagepath, tobii_controller, rotation=0, scale=1.0, brightness=1.0)














