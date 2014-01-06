import os, sys
import pygame
from random import randint, choice, sample, shuffle
from time import time

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *

WOFFSET = 200
HOFFSET = 100

screen = initialize_kelpy( dimensions=(800,600) )

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

OFF_SCREEN = (-300, -300)
ON_SCREEN = (WINDOW_WIDTH/2 + 200 , WINDOW_HEIGHT/2 + 100)

sound_yep_path = kstimulus('sounds/Beep.wav')
sound_nope_path = kstimulus('sounds/Error2.wav')

## In this task we give our user a series of items and allow them to learn the correct one.
