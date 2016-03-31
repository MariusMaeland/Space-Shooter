import pygame
from variables import *

class Bullet(pygame.sprite.Sprite):
	"""Constructor, creates a bullet fired by one of the two players."""
	def __init__(self):
		""" Constructor. Creates a bullet. Takes a
		preloaded image as imagetype. """
		super().__init__()
		self.origimage = pygame.image.load("images/bullet.png").convert_alpha()
		self.image = self.origimage.copy()
		self.rect = self.image.get_rect()
		self.bullet = []
		# Cut from the spritesheet and add them to the bullet-spritelist.
		for i in range(15):
			self.bullet.append(self.image.subsurface((i*20, 0, 20, 20)))
		self.yspeed = 0
		self.xspeed = 0
		self.dir = 0
		self.nr = 0

	def update(self, screen, all_sprites_list):
		"""Moves the bullet in the direction the  player is facing"""
		self.rect.centery += self.yspeed
		self.rect.centerx += self.xspeed
		self.animate_bullet(screen)
		if(self.rect.centerx > SCREENWIDTH):
			self.kill()
		if(self.rect.centerx < 0):
			self.kill()
		if(self.rect.centery > SCREENHEIGHT):
			self.kill()
		if(self.rect.centery < 0):
			self.kill()

	def draw(self, screen):
		game.screen.blit(self.bullet[self.nr], (self.rect.centerx, self.rect.centery))

	def animate_bullet(sprite, screen):
		"""animating the image"""
		oldCenter = sprite.rect.center
		sprite.image = sprite.bullet[sprite.nr]
		sprite.nr += 1 
		sprite.nr %= 15
		sprite.rect = sprite.image.get_rect()
		sprite.rect.center = oldCenter