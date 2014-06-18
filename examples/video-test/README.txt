The Video-Test from the kelpy library demonstrates how to record videos of your experiments.

First, as is outlined in the comments of the Video-Test.py file, you must import 
"kelpy.ScreenVideoRecorder" as a module (import kelpy.ScreenVideoRecorder)

Then, when it is time to run your experiment, rather than run it directly, you can run it using the k-record.py script provided along with this example file. 

To do this, first ensure your exeriment script, the k-record.py script, and a copy of the kelpy ScreenVideoRecorder.py script are all in the same folder. You can then run them in sequence using the k-record.py script, ex:
python k-record.py <yourexperimentscriptname>.py

All this really does is run your script then run the ScreenVideoRecorder on the file of bitmaps that it will output into this directory. If you want to handle that yourself, just ensure that you have imported the ScreenVideoRecorder module into your kelpy script. While the script runs, the video recorder will capture each frame and output a bunch of bitmaps into a new sub-directory.

The directory will be named something like "vidcap-20150503123030". This will mean that that folder and the contents were created on 05/03/2015 at 12:30:30. It will contain a bunch of bitmaps, some raw audio, and once the ScreenVideoRecorder has been run on the folder, it will also contain an OGG of the experiment audio and an avi of the audio and video of the experiment.

You can compile it by running "python ScreenVideoRecorder.py" with the name of the vidcap directory as an argument. ex:

python ScreenVideoRecorder.py exampledirectoryname

Again, if you want to save a step and just have this happen automatically, run the script using the k-record script, and pass the script to be run as an argument. It will automatically run ScreenVideoRecorder after your script has finished and compile the AVI into it's subdirectory.

voila.