echo kelpy swf export script GOOOOO
## kelpy script to render glitch assets from swf to png for use as stimuli.
# written by Matthew McGovern

########### Notes:
# this is a bash script to export a bunch of swf files to pngs. It will (should?) scale them up 6x their regular size.
# will search  1 level of subdirectories, and will only render things in the subdirectories.
## This script was originally written for use with the Glitch game assets in swf format. It is designed to be placed in the top level directory and will render everything in subdirectories of that directory.
## I used the version of Gnash that is available in the ubuntu software center. I have read that there is a better dump function in the source compiled version, but I am not sure if this is accurate. I couldn't find much in the gnash documentation about that function, or about this version of it's exporting functionality. 
## This may or may not be a dirty little secret of gnash, so use it appropriately.


counter=0
for i in $( ls ); # loops over all subfolders...
do
	## we don't want to try and open the script itself, do we?
	if [ $i != "enlarge-and-export-all-swf.sh" ]; then
		cd $i
		
		for j in $( ls );
		## look through the contents of the subfolders...
		do
		#echo $j
		
		 extension=`echo "$j" | cut -d'.' -f2`
		 filename=`echo "$j" | cut -d'.' -f1`
		 #echo $extension
			if [ "$extension" = "swf" ]; then
				#nameout = 
				
				echo exporting $j as $filename.png
				let "counter += 1"
				# The following line opens an SWF scaled 5x it's normal size, and takes a screenshot of the last frame.
				# normally it would have to play the whole file, but we also reverse it with -r1.
				# we also mark it to only play once with -1. otherwise it would loop forever.
				# Another way to do this would to omit the -1 and -r1 tags.
				## this way you would have to close the file yourself, and the last frame played would be the frame that is exported.
				gnash -s5 --screenshot last --screenshot-file $filename.png -1 -r1 $j
				
			fi
		done	
		cd ..
	fi
done
echo Finished, exported $counter files to .png 
echo Hopefully it worked! # Sorry for breaking everything!