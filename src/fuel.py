import pygame
import random
from variables import *

class Fuel(pygame.sprite.Sprite):

	def __init__(self, fuellist, x, y, width = 100, height = 100):
		""" Constructor. Creates a fuel...thingy. """
		super().__init__()
		self.posx = random.randrange(0,SCREENWIDTH, 1)
		self.posy = random.randrange(0,SCREENHEIGHT, 1)
		self.fulist = fulist
		self.image = self.fulist[0]
		self.rect = self.image.get_rect()
		self.width = width
		self.height = height
		self.rect.x = x - (self.width//2)
		self.rect.y = y - (self.height//2)
		self.nr = 0
		self.empty = False

	def update(self, screen, list):
		while not empty:
			self.image = pygame.transform.scale(self.fulist[self.nr], (self.width, self.height))
			self.nr += 1
			self.nr %= len(self.fulist)
		else:
			self.kill()
