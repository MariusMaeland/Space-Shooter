import pygame
from bullet import *

class Player(pygame.sprite.Sprite):

	def __init__(self):
		""" Constructor. Creates a player. """
		super().__init__()
		# Set the starting image
		self.origimage = pygame.transform.scale(pygame.image.load("mship1.png"), (100, 100))
		self.image = self.origimage.copy()
		self.rect = self.image.get_rect()
		# Load the image for the thruster-flame
		self.thrusterimage = pygame.image.load("thruster.png").convert_alpha()
		self.thruster = []
		self.thruster_width = 442//6
		self.nr = 0
		# Cut from the spritesheet and add them to the thruster-list.
		for x in range(6):
			self.thruster.append(self.thrusterimage.subsurface((0, x*self.thruster_width, 140, self.thruster_width)))
		# Various attributes
		self.dir = 0
		self.speed = 0
		self.thrusting = False
		self.ammo = 100000

	def thrust(self):
		"""Sets the thrust attribute to True and limits the speed"""
		if self.thrusting:
			self.speed = min(7, self.speed+1)
			self.thrusting = False

	def fire(self):
		"""Fires a shot"""
		
		#if (pygame.time.get_ticks()-self.last_shot) > (self.delay_of_fire):
		if self.ammo:
			# Restrain the rate of fire
			bullet = Bullet()
			#game.lasersound.play()
			bullet.rect.center = game.player.rect.center
			# Calculate vectors:
			actual_angle = self.dir
			actual_angle %= 360
			bullet.xspeed = math.cos(math.radians(actual_angle)) * 5
			bullet.yspeed = math.sin(math.radians(actual_angle)) * -5
        	# Add the bullets to the lists
			game.all_sprites_list.add(bullet)
			#game.bullets_list.add(bullet)
			#self.last_shot = pygame.time.get_ticks()
			# Decrease the ammo count
			self.ammo -= 1

	def turnLeft(self):
		"""Turns the ship to the left"""
		self.dir += 5
		self.dir %= 360

	def turnRight(self):
		"""Turns the ship to the right"""
		self.dir -= 5
		self.dir %= 360

	def update(self):
		rotate_sprite(self, self.dir)
		self.thrust()
		self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
		self.rect.centery -= math.sin(math.radians(self.dir)) * self.speed
		self.speed = max(0, self.speed-0.2)

	def draw(self, screen):
		pass