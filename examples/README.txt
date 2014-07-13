Demo 1: Display Something, Handle a Click.
	This is a simple demonstration of how to create an object (a CommandableImageSprite) and handle clicks on that object using the DisplayQueue, OrderedUpdates, and EventHandler classes.

Demo 2: Display a Few Things, Handle Alternatives.
	This is a slightly more complex demonstration of how to set up an array of images to create multiple CommandableImageSprites. This demonstration uses the DisplayQueue and OrderedUpdates classes to create some simple animations, and later uses the EventHandler to handle clicks on the objects. There are different responses based on whether the CommandableImageSprite is determined to be the 'correct' object or not.

Demo 3: Two Versions of the Two Alternative Forced Choice Task.
	The two versions of this program (demo3a.py and demo3b.py) demonstrate how to run a simple Two Alternative Forced Choice (2AFC) task. Two options are presented, one is preferred. When the preferred object is selected, a 'hooray!' sound is played. When the unpreferred option is selected, a 'boooo' noise is played. The data is noted through the system console, and would have to be 'piped' to be written to a file.

Demo 4: Boolean Concept Learning task.
	This demo presents the subject with stimuli and asks them to judge whether the stimuli fit a certain rule. In this case it fits the rule if the stimuli is green or a star. A purple star will fit the rule, as will a green circle or green star. A purple circle will not fit the rule.
	This demo uses a special Stimuli class to keep track of the features of the stimuli. It also uses itertools to load stimuli based on input criteria that are coded in the program. There are two lists, one of shapes, one of colors. Itertools is used to load all possible combinations of the shapes and colors.
	This demo also uses a lambda function to set 'the rule'. This allows the rule to be assigned very flexibly.

Demo 5: The blicket detector.
	This demonstration presents the subjects with a bunch of stimuli and a machine. The subject must figure out which one of the objects on screen is a 'blicket'. When the stimuli are dragged onto the machine, it will alert the subject as to whether the stimuli is a 'blicket' or not. 


Demo 5:


