import random
from variables import *
import pygame
from precode import *

class Asteroid(pygame.sprite.Sprite):
	def __init__(self, asteroidlist, width = 100, height = 100):
		super().__init__()
		self.astlist = asteroidlist
		self.image = self.astlist[0]
		self.rect = self.image.get_rect()
		
		#Set random spawn over or under the screen
		self.respawn()
		self.width = width
		self.height = height
		self.nr = 0

	def respawn(self):
		self.rect.x = random.randint(0, SCREENWIDTH)
		self.rect.y = random.choice([i for j in (range(-200, 0), range(SCREENHEIGHT, SCREENHEIGHT + 200)) for i in j])
		self.speedy = random.randint(1, 3) if self.rect.y < 0 else random.randint(-3, -1)
		self.speedx = random.randint(-3, 3)
	def update(self, screen, list):
		if self.speedy > 0:
			if self.rect.y > SCREENHEIGHT:
				self.respawn()
				#print('respawn')
		if self.speedy < 0:
			if self.rect.y < 0:
				self.respawn()
				#print('respawn')
		self.image = pygame.transform.scale(self.astlist[self.nr], (self.width, self.height))
		self.nr += 1
		self.nr %= 96
		self.rect.x += self.speedx
		self.rect.y += self.speedy
