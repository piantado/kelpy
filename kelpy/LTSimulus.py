import Image
import ImageDraw
import ImageFont

from kelpy.DotStimulus import DotStimulus

class LTStimulus(DotStimulus):
	
	
	def __init__(self, screen, letter2count, pad=30, fontpath='./FreeSans.ttf', fontsize=60):
		"""
			screen -- not implemented; if we want to render in computer experiments this should be filled in
			letter2count -- a hash of letters to how often each occurs
			pad -- how far apart are letters
			fontsize -- how big are the letters?
			
			Other options below are for colors, image size, etc. 
		
		"""
		
		# save all the passed arguments
		self.__dict__.update(locals())
	
		# We use a dotstimulus since that will already place N things on the screen so that they 
		# don't overlap
		DotStimulus.__init__(self, screen, (0,0), N=sum(letter2count.values()), area=None, radius=pad, pad=pad, height=2000, width=2000, border_width=0, border_color=(0,0,0), bg_color=(255,255,255), dot_color=None, circled=True, circle_color=(255,255,255))
		
	def to_image(self, f, width=1000, height=1000):
		# Override DotStimulus' to_image function
		
		# set up the image
		im = Image.new('RGB', (self.width, self.height))
		
		draw = ImageDraw.Draw(im)
		
		draw.rectangle( (0,0,self.width,self.height), fill=self.bg_color)
		
		if self.border_width > 0:
			draw.ellipse((0,0,self.width,self.height), fill=self.border_color)
			
		draw.ellipse((self.border_width,self.border_width,self.width-self.border_width,self.height-self.border_width), fill=self.circle_color)
		
		
		# See this: http://effbot.org/imagingbook/imagefont.htm
		font = ImageFont.truetype(self.fontpath, self.fontsize)
		
		i = 0
		#print self.dot_positions
		for let in self.letter2count.keys():
			for leti in xrange(self.letter2count[let]):
				draw.text( self.dot_positions[i], let, 'black',  font=font)
				i += 1
		
		im = im.resize((width,height), Image.ANTIALIAS) # downsize to antialias
		im.save(f)





if __name__ == "__main__":
	
	for i in xrange(10):
		
		# Generate an LTStimulus
		lts = LTStimulus(None, {'L':130, 'T':20})
		
		# Save output
		lts.to_image("LT-"+str(i)+".png")
	
	