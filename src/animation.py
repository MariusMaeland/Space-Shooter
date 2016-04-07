import pygame
import random
from variables import *

class Animation(pygame.sprite.Sprite):

	def __init__(self, animationlist, x, y, width = 100, height = 100):
		""" Constructor. Creates a health-crystal. """
		super().__init__()
		self.animationlist = animationlist.copy()
		self.image = self.animationlist[0]
		for i in range(len(animationlist)):
			self.animationlist[i] = pygame.transform.scale(self.animationlist[i], (width, height))
		self.rect = self.image.get_rect()
		self.respawn(x, y)
		self.nr = 0
		self.amount = random.randint(10,60)

	def respawn(self, x, y):
		self.rect.centerx = x
		self.rect.centery = y
		print(self.rect.center)
		

	def update(self, screen, list):
		pygame.draw.rect(screen, BLUE, self.rect, 1)
		pygame.draw.circle(screen, RED, self.rect.center, 100, 1)
		self.image = self.animationlist[self.nr]
		pygame.draw.circle(screen, YELLOW, self.rect.center, 110, 1)
		self.nr += 1
		self.nr %= len(self.animationlist)