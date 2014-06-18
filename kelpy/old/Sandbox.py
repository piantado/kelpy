# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import GIFImage

def play_image(filename, time=5.0):
    image = GIFImage.GIFImage(filename)
    screen = pygame.display.set_mode(image.get_size())

    while 1:
        screen.fill((255,255,255))
        image.render(screen, (0,0))
        pygame.display.flip()

def main():
    pygame.init()

    while 1:
        filename = "gifs/1.gif" #raw_input("filename: ")
        if filename:
            info = play_image(filename)
            print "Metadata output:\n\t", info
        else:
            return

main()