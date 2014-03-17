README for the kelpy script to render assets from 'Glitch' the game, from SWF to PNG for use as stimuli.

##############################Notes################################################33
this is a bash script to export a bunch of swf files to pngs. It will (should?) scale them up 6x their regular size.
It will search  1 level of subdirectories, and will only render things in the subdirectories.
This script was originally written for use with the Glitch game assets in swf format. It is designed to be placed in the top level directory and will render everything in subdirectories of that directory (one level deep). This was run in the 'inhabitants' subdirectory of the Glitch SWF assets, if you are interested in dupliating these results.
I used the version of Gnash that is available in the ubuntu software center. I have read that there is a better dump function in the source compiled version, but I am not sure if this is accurate. I couldn't find much in the gnash documentation about that function, or about this version of it's exporting functionality.

*Most of the script is just an excuse to run this command:

gnash -s5 -t.1 -r1 --screenshot last --screenshot-file $filename.png $j

gnash : the program gnash.
-s5   : argument to scale the image 5x it's normal size (they were pretty small to start out).
--screenshot last : takes a screenshot of the last frame played.
--screenshot-file : names the output file (I use a variable named $filename.png to keep the original name.)
-t.1  : argument to end the file after .1 second (any quicker results in undesired rendering behavior)
-r1  : rendering mode 1, image rendering is enabled, sound rendering is disabled.
$j   : this is a variable that ends up being the name of the file we want to render, which is the input .swf file.

*Closely followed by this command:
convert -transparent white $filename.png $filename.png

*The command uses imagemagick (again from the ubuntu software center) to rerender the png image to exlude the white background. Not all the images I dealt with in the glitch asset library had white backgrounds, but it was enough where I could put the rest into gimp and remove them one by one without too much trouble.

*If you need to modify that command, just be aware the input file is the one on the left, the output filename on the right. In this case we are just overwriting the same file, so they are the same.



*The rest deals with the moving around between subdirectories and checking for swf files to render.

*The two commands inside the following for loop are used to split up a filename from it's extension, so that we can check the extension to see if it needs to be rendered, and then later to name the output file if it does end up getting rendered.

for j in $( ls ); do    ### << lists all the files in the subdirectory
extension=`echo "$j" | cut -d'.' -f2`  ### <<---- echo the file, piped into 'cut', store the second half after the period.
filename=`echo "$j" | cut -d'.' -f1`   ### <<---- echo the file, piped into the program 'cut', store the first half before the period.

*If you are dealing with filenames with a bunch of periods, this part of the script will need to be modified.

*That's pretty much the entire script! Feel free to modify to suit your needs!


-mm				
