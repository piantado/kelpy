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


**Tobii SDK Installation**
The Tobii SDK can be downloaded at `their website <http://www.tobiipro.com/product-listing/tobii-pro-analytics-sdk/>`_.
In the zip folder, extract the version that matches your OS (including if it's 32 or 64-bit), rename the folder to ``tobiisdk``, and place it in the same parent directory as the kelpy library. So sticking with our example, it would be in:

	/home/piantado/mit/Libraries/tobiisdk/

Add the following path to your ``PYTHONPATH`` environment variable (as you did previously for adding kelpy):

	export PYTHONPATH=$PYTHONPATH:/home/piantado/Desktop/mit/Libraries/tobiisdk/python27/modules


For Linux users, you will also need to install the following additional python modules(using ``apt-get install``):

+ libssh2-1
+ libavahi-client3

See the Tobii SDK Developers Guide that came with the SDK for more information, if curious.


