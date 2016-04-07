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
		self.pos = Vector2D(random.randint(0, SCREENWIDTH),random.choice([i for j in (range(-200, 0), range(SCREENHEIGHT, SCREENHEIGHT + 200)) for i in j]))
		self.speed = Vector2D(random.randint(-3, 3),random.randint(1, 3) if self.rect.y < 0 else random.randint(-3, -1))
		self.width = width
		self.height = height
		self.radius = (width//2)-17
		self.nr = 0
		
	def respawn(self):
		self.pos.x = random.randint(0, SCREENWIDTH)
		self.pos.y = random.choice([i for j in (range(-200, 0), range(SCREENHEIGHT, SCREENHEIGHT + 200)) for i in j])
		self.speed.x = random.randint(-3, 3)
		self.speed.y = random.randint(1, 3) if self.rect.y < 0 else random.randint(-3, -1)
	def update(self, screen, list):
		if self.speed.y > 0:
			if self.rect.top > SCREENHEIGHT:
				self.respawn()
				#print('respawn')
		if self.speed.y < 0:
			if self.rect.bottom < 0:
				self.respawn()
				#print('respawn')
		self.image = pygame.transform.scale(self.astlist[self.nr], (self.width, self.height))
		self.nr += 1
		self.nr %= 96
		
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		
		if self.speed.magnitude() > ASTEROIDSMAXSPEED:
			self.speed = self.speed.normalized() * ASTEROIDSMAXSPEED
		if self.speed.magnitude() < ASTEROIDSMINSPEED:
			self.speed = self.speed.normalized() * ASTEROIDSMINSPEED
		self.pos += self.speed

