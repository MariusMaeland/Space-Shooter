import pygame
from config import *

class Explosion(pygame.sprite.Sprite):
	"""Animates an explosion"""
	def __init__(self, explosionlist, x, y, width = 100, height = 100):
		""" Constructor. Creates an explosion. 
			Takes in list of sprites, position and scale."""
		super().__init__()
		self.explist = explosionlist
		self.image = self.explist[0]
		self.rect = self.image.get_rect()
		self.width = width
		self.height = height
		self.rect.x = x - (self.width//2)
		self.rect.y = y - (self.height//2)
		self.nr = 0

	def update(self, screen, list):
		"""Iterates through animation list and removes it self when done."""
		if self.nr < len(self.explist):
			self.image = pygame.transform.scale(self.explist[self.nr], (self.width, self.height))
			self.nr += 1
		else:
			self.kill()
