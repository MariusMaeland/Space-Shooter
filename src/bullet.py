import pygame
from config import *

class Bullet(pygame.sprite.Sprite):
	"""Constructor, creates a bullet fired by one of the two players."""
	def __init__(self, bulletlist, direction):
		""" Constructor. Creates a bullet. """
		super().__init__()
		self.bullet = bulletlist.copy()
		self.origimage = self.bullet[0]
		self.image = self.origimage.copy()
		self.rect = self.image.get_rect()
		self.dir = direction
		self.yspeed = 0
		self.xspeed = 0
		self.nr = 0

	def update(self, screen, all_sprites_list):
		"""Moves the bullet in the direction the  player is facing"""
		self.rect.centery += self.yspeed
		self.rect.centerx += self.xspeed
		self.animate_bullet(screen, self.dir)
		if(self.rect.centerx > SCREENWIDTH):
			self.kill()
		if(self.rect.centerx < 0):
			self.kill()
		if(self.rect.centery > SCREENHEIGHT):
			self.kill()
		if(self.rect.centery < 0):
			self.kill()

	def animate_bullet(sprite, screen, degrees):
		"""animating the image"""
		oldCenter = sprite.rect.center
		sprite.image = pygame.transform.rotate(sprite.bullet[sprite.nr], degrees)
		sprite.nr += 1 
		sprite.nr %= 11
		sprite.rect = sprite.image.get_rect()
		sprite.rect.center = oldCenter