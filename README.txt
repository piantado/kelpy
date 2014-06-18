Kelpy


KELPY is the Kid Experimental Library in PYthon

Installation
Put this library somewhere--mine lives in "/home/piantado/mit/Libraries/kelpy/"


Set the PYTHONPATH environment variable to point to LOTlib/:

	export PYTHONPATH=$PYTHONPATH:/home/piantado/Desktop/mit/Libraries/kelpy

You can put this into your .bashrc file to make it load automatically when you open a terminal. On ubuntu and most linux, this is:

	echo 'export PYTHONPATH=$PYTHONPATH:/home/piantado/Desktop/mit/Libraries/kelpy' >> ~/.bashrc


And you should be ready to use the library

About
The basic approach of Kelpy is to handle simple animations and things, taking care of the main refresh-display loop in pygame, and letting us just construct sequences of object actions and handle events. Future work will handle fancier counterbalancing, etc. 

*Kelpy is a work in progress, so please be mindful that some demos and classes may not function as intended just yet!*


Dependencies:
	
+	PIL
+	Pygame
+	Tobii SDK

Credits:

Steven T. Piantadosi, Matthew McGovern, and Amanda Yung are the primary contributors to this project.


Citation:

This software may be cited as:

	@misc{piantadosi2012kelpy,
	author={Steven T. Piantadosi},
	title={ Kelpy: a free library for child experimentation in python},
	year={2012},
	howpublished={available from https://github.com/piantado/kelpy/ }
	} 
