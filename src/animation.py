import pygame
import random
from variables import *

class Animation(pygame.sprite.Sprite):

	def __init__(self, animationlist, x, y, width = 100, height = 100):
		""" Constructor. Creates fuel, and ammo crystals. """
		super().__init__()
		self.animationlist = animationlist.copy()
		self.image = self.animationlist[0]
		for i in range(len(animationlist)):
			self.animationlist[i] = pygame.transform.scale(self.animationlist[i], (width, height))
		self.rect = self.image.get_rect()
		self.respawn(x, y)
		self.nr = 0
		self.fuelamount = random.randint(30,60)
		self.hpamount = random.randint(10,60)
		self.ammoamount = 20

	def respawn(self, x, y):
		"""makes the crystals respawn at random location after picked up"""
		self.rect.centerx = x
		self.rect.centery = y
		print(self.rect.center)
		

	def update(self, screen, list):
		"""updates and animates the sprites"""
		if DEBUG:
			pygame.draw.rect(screen, BLUE, self.rect, 1)
			pygame.draw.circle(screen, RED, self.rect.center, 100, 1)
		self.image = self.animationlist[self.nr]
		if DEBUG:
			pygame.draw.circle(screen, YELLOW, self.rect.center, 110, 1)
		self.nr += 1
		self.nr %= len(self.animationlist)