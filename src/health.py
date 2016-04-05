import pygame
import random
from variables import *

class Health(pygame.sprite.Sprite):

	def __init__(self, crystallist, width = 134//3, height = 128//3):
		""" Constructor. Creates a health-crystal. """
		super().__init__()
		self.crystallist = crystallist
		self.image = self.crystallist[0]
		self.rect = self.image.get_rect()
		self.respawn()
		self.width = width
		self.height = height
		self.nr = 0
		self.amount = random.randint(10,60)

	def respawn(self):
		self.rect.x = random.randint((0+SCREENWIDTH//3),(SCREENWIDTH-SCREENWIDTH//3))
		self.rect.y = random.randint((0+SCREENHEIGHT//3),(SCREENHEIGHT-SCREENHEIGHT//3))
		

	def update(self, screen, list):
		self.image = pygame.transform.scale(self.crystallist[self.nr], (self.width, self.height))
		self.nr += 1
		self.nr %= len(self.crystallist)