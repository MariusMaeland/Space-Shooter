import random
from config import *
import pygame
from precode import *

class Asteroid(pygame.sprite.Sprite):
	def __init__(self, asteroidlist, width = 100, height = 100):
		"""Constructor for the Asteroid class
		Takes a preloaded list of images and optional scale.
		An instance will spawn somewhere off screen and then be given
		a random direction towards the player-area on the screen."""	
		super().__init__()
		self.astlist = asteroidlist
		self.image = self.astlist[0]
		self.rect = self.image.get_rect()
		self.pos = Vector2D(random.randint(0, SCREENWIDTH),random.choice([i for j in (range(-200, 0), range(SCREENHEIGHT, SCREENHEIGHT + 200)) for i in j]))
		self.speed = Vector2D(random.randint(-3, 3),random.randint(1, 3) if self.rect.y < 0 else random.randint(-3, -1))
		self.width = width
		self.height = height
		self.radius = (width//2)-17
		self.nr = 0
		self.hp = 3
		
	def respawn(self):
		"""Moves the asteroid outside the screen, giving it new startpos and speed"""
		self.pos.x = random.randint(0, SCREENWIDTH)
		self.pos.y = random.choice([i for j in (range(-200, 0), range(SCREENHEIGHT, SCREENHEIGHT + 200)) for i in j])
		self.speed.x = random.randint(-3, 3)
		self.speed.y = random.randint(2, 3) if self.rect.y < 0 else random.randint(-3, -2)
		self.hp = 3
	def update(self, screen, list):
		"""Updating the position to the asteroid and handling speed limit"""
		# Check if the asteroids fly off the screen
		if self.speed.y > 0:
			if self.rect.top > SCREENHEIGHT:
				self.respawn()
		if self.speed.y < 0:
			if self.rect.bottom < 0:
				self.respawn()
		
		# Move to the next image in the animation
		self.animate()
	
		
		# Move the rect to the vectors position
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y
		
		# Limit the speed-vector
		if self.speed.magnitude() > ASTEROIDSMAXSPEED:
			self.speed = self.speed.normalized() * ASTEROIDSMAXSPEED
		if self.speed.magnitude() < ASTEROIDSMINSPEED:
			self.speed = self.speed.normalized() * ASTEROIDSMINSPEED
		self.pos += self.speed
		
		self.gravitation()

	def gravitation(self):
		"""Calculates gravitational pull on the asteroid"""
		direction = BLACKHOLEPOS-self.pos
		self.speed += direction.normalized()*4/(direction.magnitude())

	def animate(self):
		"""Loops through a list of images cut from a sprite-sheet."""
		self.image = pygame.transform.scale(self.astlist[self.nr], (self.width, self.height))
		self.rect = self.image.get_rect()
		self.nr += 1
		self.nr %= 96