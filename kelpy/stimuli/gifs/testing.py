import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import VideoFileClip
import pygame

pygame.display.set_caption('My video!')

clip = VideoFileClip('babylaugh.mov')
clip.preview()
pygame.quit()
