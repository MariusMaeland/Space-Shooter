import random
from variables import *
import pygame
from precode import *

class Asteroid(pygame.sprite.Sprite):
	def __init__(self, asteroidlist, width = 100, height = 100):
		super().__init__()
		self.posx = random.randrange(0, SCREENWIDTH, 1)
		self.posy = -10
		#Set random spawn over or under the screen
		self.random_spawn = random.randrange(0, 10, 1)
		self.random_speedx = random.randrange(-3, 3, 1)
		self.speedx = self.random_speedx
		self.speedy = 0
		if self.random_spawn > 5:
			self.posy = random.randrange(-200, 0, 1)
			self.speedy = random.randrange(1, 3, 1)
		if self.random_spawn < 5:
			self.posy = random.randrange(SCREENHEIGHT, SCREENHEIGHT+200, 1)
			self.random_speedy = random.randrange(-3, -1, 1)
			self.speedy = self.random_speedy
		
		#self.pos = Vector2D(self.posx, self.posy)
		#self.random_speed = random.randrange(-3, 3)
		#self.speed = Vector2D(self.speedx, self.speedy)
		
		self.astlist = asteroidlist
		self.image = self.astlist[0]
		self.rect = self.image.get_rect()
		self.width = width
		self.height = height
		self.rect.x = self.posx - (self.width//2)
		self.rect.y = self.posy - (self.height//2)
		self.nr = 0
	
	def update(self, screen, list):
		
		self.image = pygame.transform.scale(self.astlist[self.nr], (self.width, self.height))
		self.nr += 1
		self.nr %= 96
		self.rect.x += self.speedx
		self.rect.y += self.speedy