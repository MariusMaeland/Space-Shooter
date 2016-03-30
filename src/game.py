import pygame
import random
import math
from variables import *
from Bullet import *
from Player import *

class Game():
	"""Initializes the game and handles user input, loading, pausing etc..."""
	def __init__(self):
		# Initialize pygame
		pygame.init()
		# Naming the display surface
		self.screen = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
		# Setting the caption of window
		pygame.display.set_caption(CAPTION, 'Space')
		# Setting up sound
		pygame.mixer.init()
		# ----------- VARIOUS LOADING --------------------
		self.clock = pygame.time.Clock()
		self.background = pygame.image.load("space.png")

	def setup(self):
		# -------------------- 360 Controller Works --------------------------
		print('Setting up joystick...')
		self.joystick_count = pygame.joystick.get_count()
		if self.joystick_count == 0:
			print("Error, no joystick found!")
		else:
			for i in range(self.joystick_count):
				self.joystick = pygame.joystick.Joystick(i)
				self.joystick.init()
				self.joystick_name = self.joystick.get_name()
				print(self.joystick_name)
		
		self.all_sprites_list = pygame.sprite.Group()
		self.player = Player()
		self.all_sprites_list.add(self.player)

	def eventhandler(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		
		# Getting keyboard array:
		self.pressed = pygame.key.get_pressed()
		# Checking for keys and calling the wanted movement:
		# Quit:
		if self.pressed[pygame.K_ESCAPE]:
			exit()
		if self.pressed[pygame.K_a]:
			self.player.animate(self.screen)
		if self.pressed[pygame.K_RIGHT]:
			self.player.turnRight()
		if self.pressed[pygame.K_LEFT]:
			self.player.turnLeft()
		if self.pressed[pygame.K_UP]:
			self.player.thrusting = True
		if self.pressed[pygame.K_KP0]:
			self.player.fire()
		



	def run(self):
			"""Runs an instance of itself..."""
			self.setup()
			while True:
				while GAME_STATE:
					# Set background to space image
					self.screen.blit(self.background, (0, 0))
					# Handling events
					self.eventhandler()
					self.all_sprites_list.update()
					self.all_sprites_list.draw(self.screen)
					
					pygame.display.flip()
					# Limit to 60 frames per second
					self.clock.tick(FPS)

# ---------------------------------------------------
#                  MAIN PROGRAM LOOP 
# ---------------------------------------------------

if __name__ == "__main__":
	game = Game()
	game.run()