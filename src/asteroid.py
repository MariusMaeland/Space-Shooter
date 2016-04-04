import random
from variables import *
import pygame

class Asteroid(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.posx = random.randrange(0, SCREENWIDTH)
		self.random_spawn = random.randrange(1, 2)
		if self.random_spawn == 1:
			self.posy = random.randrange(0, -200)
		if self.random_spawn == 2:
			self.posy = random.randrange(SCREENHEIGHT, SCREENHEIGHT+200)
		self.pos = Vector2D(self.posx, self.posy)