import pygame
from variables import *

class Explosion(pygame.sprite.Sprite):

	def __init__(self, explosionlist, x, y, width = 100, height = 100):
		""" Constructor. Creates an explosion. """
		super().__init__()
		self.explist = explosionlist
		self.image = self.explist[0]
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.width = width
		self.height = height
		self.nr = 0

	def update(self, screen, list):
		if self.nr < len(self.explist):
			self.image = pygame.transform.scale(self.explist[self.nr], (self.width, self.height))
			print(self.rect.centerx)
			print(self.rect.centery)
			#screen.blit(self.image, (self.rect.centerx, self.rect.centery))
			self.nr += 1
		else:
			self.kill()
