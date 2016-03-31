import pygame
from bullet import Bullet
import math
import random
from variables import *

class Player(pygame.sprite.Sprite):

	def __init__(self, startx, starty, start_angle):
		""" Constructor. Creates a player. """
		super().__init__()
		# Set the starting image
		self.origimage = pygame.transform.scale(pygame.image.load(random.choice(ship_image_list)), (50, 50))
		self.image = self.origimage.copy()
		self.rect = self.image.get_rect()
		self.rect.center = (startx, starty)
		# Load the image for the thruster-flame
		self.thrusterimage = pygame.image.load("images/jetflame.png").convert_alpha()
		self.thruster = []
		self.thruster_width = 1920//30
		self.nr = 0
		# Cut from the spritesheet and add them to the thruster-list.
		for i in range(30):
			self.thruster.append(self.thrusterimage.subsurface((i*self.thruster_width, 0, self.thruster_width, self.thruster_width)))
		# Various attributes
		self.dir = start_angle
		self.speed = 0
		self.thrusting = False
		# Various ammo-related stuff
		self.ammo = 100000
		self.last_shot = 0
		self.rate_of_fire = 100

	def thrust(self):
		"""Sets the thrust attribute to True and limits the speed"""
		if self.thrusting:
			self.speed = min(7, self.speed+1)
			self.thrusting = False

	def fire(self, all_sprites_list):
		"""Fires a shot, takes in all_sprites_list to get access to the group
		Firing is limited by the self.rate of fire(compulsory time in milliseconds
		between each shot). """
		
		# Restrain the rate of fire
		if (pygame.time.get_ticks()-self.last_shot) > (self.rate_of_fire):
			if self.ammo:
				bullet = Bullet()
				#game.lasersound.play()
				bullet.rect.centerx = self.rect.centerx
				bullet.rect.centery = self.rect.centery
				# Calculate vectors:
				bullet.xspeed = math.cos(math.radians(self.dir)) * 10
				bullet.yspeed = math.sin(math.radians(self.dir)) * -10
	        	# Add the bullets to the lists
				all_sprites_list.add(bullet)
				self.last_shot = pygame.time.get_ticks()
				# Decrease the ammo count
				self.ammo -= 1

	def turnLeft(self):
		"""Turns the ship to the left"""
		self.dir += 1
		self.dir %= 360

	def turnRight(self):
		"""Turns the ship to the right"""
		self.dir -= 1
		self.dir %= 360

	def update(self, screen, all_sprites_list):
		self.rotate_sprite(self.dir)
		self.thrust()
		self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
		self.rect.centery -= math.sin(math.radians(self.dir)) * self.speed
		self.speed = max(0, self.speed-0.2)

	def rotate_sprite(sprite, degrees):
		"""Rotating the image and rect"""
		#get original center because new Rect center will change with image transformation
		oldCenter = sprite.rect.center
		flamey_ship = pygame.Surface((200, 100))
		pygame.draw.rect(flamey_ship, (255,0,0), flamey_ship.get_rect(), 1)
		if sprite.thrusting:
			flamey_ship.blit(sprite.thruster[sprite.nr], (25, 20))
		sprite.nr += 1
		sprite.nr %= 30
		flamey_ship.blit(sprite.origimage, (75,25))
		flamey_ship.set_colorkey((0,0,0))
		#use pygame.transform.rotate(<image_to_rotate>, <turn_degrees>)
		sprite.image = pygame.transform.rotate(flamey_ship, degrees)
		#get new Rect
		sprite.rect = sprite.image.get_rect()
		#set new center to original center
		sprite.rect.center = oldCenter
	
	def draw(self, screen):
		pass