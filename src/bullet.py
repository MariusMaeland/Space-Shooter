import pygame
from functions import *

class Bullet(pygame.sprite.Sprite):
	"""Constructor, creates a bullet fired by one of the two players."""
	def __init__(self):
		""" Constructor. Creates a bullet. Takes a
		preloaded image as imagetype. """
		super().__init__()
		self.origimage = pygame.image.load("images/bullets.png").convert_alpha()
		self.image = self.origimage.copy()
		self.rect = self.image.get_rect()
		self.bullet = []
		# Cut from the spritesheet and add them to the bullet-spritelist.
		for i in range(30):
			self.bullet.append(self.image.subsurface((i*64, 0, 64, 64)))
		self.yspeed = 0
		self.xspeed = 0
		self.dir = 0
		self.nr = 0

	def update(self, screen):
		"""Moves the bullet in the direction the  player is facing"""
		self.rect.centery += self.yspeed
		self.rect.centerx += self.xspeed
		self.rotate_bullet(self.dir, screen)

	def draw(self, screen):
		game.screen.blit(self.bullet[self.nr], (self.rect.centerx, self.rect.centery))

	def rotate_bullet(sprite, degrees, screen):
		"""Rotating the image and rect"""
		#get original center because new Rect center will change with image transformation
		oldCenter = sprite.rect.center
		#shot = pygame.Surface((100, 100))
		#pygame.draw.rect(flamey_ship, (255,0,0), flamey_ship.get_rect(), 1)
		
		#screen.blit(sprite.bullet[sprite.nr], (sprite.rect.centerx, sprite.rect.centery))
		#shot.blit(sprite.origimage, (150,50))
		#shot.set_colorkey((0,0,0))
		#use pygame.transform.rotate(<image_to_rotate>, <turn_degrees>)
		sprite.image = pygame.transform.rotate(sprite.bullet[sprite.nr], degrees)
		sprite.nr += 1
		sprite.nr %= 30
		#get new Rect
		sprite.rect = sprite.image.get_rect()
		#set new center to original center
		sprite.rect.center = oldCenter