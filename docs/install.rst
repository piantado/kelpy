Installation
============

Put this library somewhere--mine lives in::

/home/piantado/mit/Libraries/kelpy/


Set the ``PYTHONPATH`` environment variable to point to the library::

	export PYTHONPATH=$PYTHONPATH:/home/piantado/Desktop/mit/Libraries/kelpy

You can put this into your .bashrc file to make it load automatically when you open a terminal. On ubuntu and most linux, this is::

	echo 'export PYTHONPATH=$PYTHONPATH:/home/piantado/Desktop/mit/Libraries/kelpy' >> ~/.bashrc

	PYTHONPATH="${PYTHONPATH}:/path/to/some/cool/python/package/:/path/to/another/cool/python/package/"
	export PYTHONPATH


Dependencies
-------------

+	PIL
+	Pygame
+	Tobii SDK (optional -- for Tobii eye tracker integration)
