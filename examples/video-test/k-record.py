import sys,os
from sys import *
import datetime
from kelpy.ScreenVideoRecorder import lastdir

"""
This is a script to run a kelpy script and record a video of the experiment in progress.
It requires that you input the filename of the script you want to run as an argument.

python runkelpy.py <yourscriptname>.py  <<< exactly like this. removing the < > and replacing yourscriptname with your script name (of course).


"""

run_script = None
print "Attempting to run your kelpy script!"
if len(sys.argv)==1:
	##You didn't input the filename!
	print "ERROR: no filename passed as an argument."
	print "       please input the filename of the script you wish to run."
	print "       example syntax: python runkelpy.py <yourscriptname>.py "
	sys.exit()
else:
	print "Checking for your kelpy script's name..."
	for i in range(len(sys.argv)):
		## Check the arguments. right now we only handle one, the filename, but this could be improved later to handle more stuff.
		##print argv[i] , i
		if argv[i].rsplit('.', 1)[1]=='py' and argv[i].rsplit('.', 1)[0] !="runkelpy":
			run_script = argv[i]
			print "Found " + run_script

##print run_script

if run_script is not None:
	print "Attemting to run " + run_script
	os.system("python " + run_script)
	print "Run (should have) finished. Proceeding to render video."

video_directory = lastdir()
if video_directory is not None:
	print "Compiling AVI from " + video_directory
	for d in os.listdir("."):
		if d.startswith("ScreenVideoRecorder"):
			os.system("python ScreenVideoRecorder.py " + video_directory)