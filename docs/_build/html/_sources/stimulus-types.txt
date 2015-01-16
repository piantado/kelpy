.. _stimulus-types:

Stimulus Types
================

There are several different types of stimuli in kelpy. Here is an overview of the types:

Sprites
------------

CommandableImageSprite
~~~~~~~~~~~~~~~~~~~~~~~~

DragSprite
~~~~~~~~~~~~~~~~~~~~~~~~

DropSprite
~~~~~~~~~~~~~~~~~~~~~~~~

TextSprite
~~~~~~~~~~~~~~~~~~~~~~~~


Other Visuals
----------------

AttentionGetter
~~~~~~~~~~~~~~~~~~~~~~~



Sounds
----------------

Sounds are simply played using ``play_sound()``:

.. code-block:: python

	play_sound(kstimulus('sounds/Tada.wav'), wait=True, volume=0.8)