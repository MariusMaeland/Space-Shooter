import random
from variables import *
import pygame

class Asteroid(pygame.sprite.Sprite):
	
	def __init__(self, asteroidlist, x, y, width = 100, height = 100):
		super().__init__()
		#self.posx = random.randrange(0, SCREENWIDTH)
		# Set random spawn over or under the screen
		#self.random_spawn = random.randrange(1, 2)
		#if self.random_spawn == 1:
		#	self.posy = random.randrange(0, -200)
		#if self.random_spawn == 2:
		#	self.posy = random.randrange(SCREENHEIGHT, SCREENHEIGHT+200)
		self.astlist = asteroidlist
		#self.pos = Vector2D(self.posx, self.posy)
		self.image = self.astlist[0]
		self.rect = self.image.get_rect()
		self.width = width
		self.height = height
		self.rect.x = x - (self.width//2)
		self.rect.y = y - (self.height//2)
		self.nr = 0
		#self.random_speed = random.randrange(-3, 3)
		#self.speedx = self.random_speed
		#self.speedy = self.random_speed
		#self.speed = Vector2D(self.speedx, self.speedy)
	
	def update(self, screen, list):
		self.image = pygame.transform.scale(self.astlist[self.nr], (self.width, self.height))
		self.nr += 1
		self.nr %= 64