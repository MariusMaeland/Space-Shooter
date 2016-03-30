import pygame

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

	def update(self):
		"""Moves the bullet in the direction the  player is facing"""
		self.rect.centery += self.yspeed
		self.rect.centerx += self.xspeed

	def draw(self, screen):
		game.screen.blit(self.bullet[self.nr], (self.rect.centerx, self.rect.centery))