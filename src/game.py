#!/usr/bin/env python3
import pygame
import random
import math
from variables import *
from bullet import Bullet
from player import Player
from explosion import Explosion

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
		self.background = pygame.image.load("images/space.png")

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
		
		#-----------------------------------------------------------------------
		#                    SETTING UP EXPLOSION-SHEET
		#-----------------------------------------------------------------------
		self.explosion_image = pygame.image.load("images/explosion.png").convert_alpha()
		self.explosion_list = []
		self.esw = 1024//10 # Divide by ten because there are ten images per row on the sheet. ESW = explosion sheet witdh.
		for i in range(8): # Because there are 8 rows of images on the sheet 
			for j in  range(10): # Ten images per row on the sprite sheet
				self.explosion_list.append(self.explosion_image.subsurface(j*self.esw, i*self.esw, self.esw, self.esw))
		print(len(self.explosion_list))

		#-----------------------------------------------------------------------
		#                    SETTING UP SPRITEGROUPS
		#-----------------------------------------------------------------------
		self.all_sprites_list = pygame.sprite.Group()
		self.player1_bullets = pygame.sprite.Group()
		self.player2_bullets = pygame.sprite.Group()
		self.fuel_list = pygame.sprite.Group()
		self.asteroid_list = pygame.sprite.Group()

		self.player1 = Player(50, SCREENHEIGHT//2, 0)
		self.player2 = Player(SCREENWIDTH -50, SCREENHEIGHT//2, 180)
		self.all_sprites_list.add(self.player1)
		self.all_sprites_list.add(self.player2)
		self.death = Explosion(self.explosion_list, 600, 350, 200, 200)
		self.all_sprites_list.add(self.death)

	def collisionchecks(self):
		for bullet in self.player1_bullets:
			if pygame.sprite.collide_mask(bullet, self.player2):
				self.death = Explosion(self.explosion_list, self.player2.rect.centerx, self.player2.rect.centery)
				self.all_sprites_list.add(self.death)
				self.player2.kill()
				# TODO: Animate explosion in killpos!
				bullet.kill()
				self.setup()
		for bullet in self.player2_bullets:
			if pygame.sprite.collide_mask(bullet, self.player1):
				self.player1.kill()
				# TODO: Animate explosion in killpos!
				bullet.kill()
				self.setup()
		if pygame.sprite.collide_mask(self.player1, self.player2):
				self.player1.kill()
				self.player2.kill()
				self.setup()

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
		if self.pressed[pygame.K_RIGHT]:
			self.player1.turnRight()
		if self.pressed[pygame.K_LEFT]:
			self.player1.turnLeft()
		if self.pressed[pygame.K_UP]:
			self.player1.thrusting = True
		if self.pressed[pygame.K_KP0]:
			self.player1.fire(self.all_sprites_list, self.player1_bullets)

		if self.pressed[pygame.K_d]:
			self.player2.turnRight()
		if self.pressed[pygame.K_a]:
			self.player2.turnLeft()
		if self.pressed[pygame.K_w]:
			self.player2.thrusting = True
		if self.pressed[pygame.K_q]:
			self.player2.fire(self.all_sprites_list, self.player2_bullets)

	def run(self):
			"""Runs an instance of itself..."""
			self.setup()
			while True:
				while GAME_STATE:
					# Set background to space image
					self.screen.blit(self.background, (0, 0))
					# Handling events
					self.eventhandler()
					self.all_sprites_list.update(self.screen, self.all_sprites_list)
					self.all_sprites_list.draw(self.screen)
					self.collisionchecks()
					pygame.display.flip()
					# Limit to 60 frames per second
					self.clock.tick(FPS)

# ---------------------------------------------------
#                  MAIN PROGRAM LOOP 
# ---------------------------------------------------

if __name__ == "__main__":
	game = Game()
	game.run()