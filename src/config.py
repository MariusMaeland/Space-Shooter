import pygame
from precode import *
"""A collection of all the global variables used in the game"""

SCREENWIDTH = 1200 # Width of the window
SCREENHEIGHT = 800 # Height of the window
CAPTION = 'Space Shooter'
FPS = 60
GAME_STATE = True
DEBUG = False

BLACKHOLEPOS = Vector2D(SCREENWIDTH//2, SCREENHEIGHT//2)
GRAVITY = 100

# Player related globals
TIMETORESPAWN = 3
INVINCIBLETIME = 4

P1STARTPOS = (50, SCREENHEIGHT//2)
P1STARTANGLE = 0
P1DEADPOS = (-500, -500)


P2STARTPOS = (SCREENWIDTH - 50, SCREENHEIGHT//2)
P2STARTANGLE = 180
P2DEADPOS = (SCREENWIDTH + 500, SCREENHEIGHT + 500)

BULLETSPEED = 15
PLAYERMAXSPEED = 4
ship_image_list = ["images/ship1.png", "images/ship2.png", "images/ship3.png", "images/ship4.png"]

# Asteroid stuff
ASTEROIDSNUM = 6	
ASTEROIDSMAXSPEED = 4
ASTEROIDSMINSPEED = 2

# Pick ups
FUELNUM = 1
HEALTHNUM = 1
AMMONUM = 1

# Some colors
BLACK      = (   0,   0,   0)
WHITE      = ( 255, 255, 255)
GREEN      = (   0, 255,   0)
RED        = ( 255,   0,   0)
BLUE       = (   0,   0, 255)
BROWN      = ( 138, 115,  76)
ORANGE     = ( 255, 128,   0)
YELLOW     = ( 255, 255,   0)
LIGHTGREEN = ( 128, 255,   0)
DARKGREEN  = (   0, 204,   0)
TEAL       = (   0, 255, 255)
LIGHTBLUE  = (   0, 128, 255)
DARKBLUE   = (   0,   0, 255)
PURPLE     = ( 128,   0, 255)
PINK       = ( 255,   0, 255)
WARMPINK   = ( 255,   0, 128)
GREY       = ( 160, 160, 160)

