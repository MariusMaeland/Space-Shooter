import pygame
import random
import math
import itertools
from variables import *
from spritesheetfunctions import SpriteSheet


class Player(pygame.sprite.Sprite):

	def __init__(self):
		""" Constructor. Creates a character. """
		super().__init__()
		# Set the starting image
		self.origimage = pygame.transform.scale(pygame.image.load("mship1.png"), (100, 100))
		self.image = self.origimage.copy()
		self.rect = self.image.get_rect()
		# Load the image for the thruster-flame
		self.thrusterimage = pygame.image.load("thruster.png").convert_alpha()
		self.thruster = []
		self.thruster_width = 442//6
		self.nr = 0
		# Cut from the spritesheet and add them to the thruster-list.
		for x in range(6):
			self.thruster.append(self.thrusterimage.subsurface((0, x*self.thruster_width, 140, self.thruster_width)))
		# Various attributes
		self.dir = 0
		self.speed = 0
		self.thrusting = False
		self.ammo = 100000

	def thrust(self):
		if self.thrusting:
			self.speed = min(7, self.speed+1)
			self.thrusting = False

	def fire(self):
		"""Handling shooting with the a-button"""
		
		#if (pygame.time.get_ticks()-self.last_shot) > (self.delay_of_fire):
		if self.ammo:
			# Restrain the rate of fire
			bullet = Bullet()
			#game.lasersound.play()
			bullet.rect.center = game.player.rect.center
			# Calculate vectors:
			actual_angle = self.dir
			actual_angle %= 360
			bullet.xspeed = math.cos(math.radians(actual_angle)) * 5
			bullet.yspeed = math.sin(math.radians(actual_angle)) * -5
        	# Add the bullets to the lists
			game.all_sprites_list.add(bullet)
			#game.bullets_list.add(bullet)
			#self.last_shot = pygame.time.get_ticks()
			# Decrease the ammo count
			self.ammo -= 1

	def turnLeft(self):
		self.dir += 5
		self.dir %= 360

	def turnRight(self):
		self.dir -= 5
		self.dir %= 360

	def update(self):
		rotate_sprite(self, self.dir)
		self.thrust()
		self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
		self.rect.centery -= math.sin(math.radians(self.dir)) * self.speed
		self.speed = max(0, self.speed-0.2)

	def draw(self, screen):
		pass

def animate(surface, spritelist, x, y):
	nr = 0
	for image in range(len(spritelist)-1):
		surface.blit(spritelist[nr], (x, y))
		nr += 1
		nr %= len(spritelist)-1

def rotate_sprite(sprite, degrees):
	"""Rotating the image and rect"""
	#get original center because new Rect center will change with image transformation
	oldCenter = sprite.rect.center
	flamey_ship = pygame.Surface((400, 200))
	#pygame.draw.rect(flamey_ship, (255,0,0), flamey_ship.get_rect(), 1)
	if sprite.thrusting:
		flamey_ship.blit(sprite.thruster[sprite.nr], (25, 60))
	sprite.nr += 1
	sprite.nr %= 6
	flamey_ship.blit(sprite.origimage, (150,50))
	flamey_ship.set_colorkey((0,0,0))
	#use pygame.transform.rotate(<image_to_rotate>, <turn_degrees>)
	sprite.image = pygame.transform.rotate(flamey_ship, degrees)
	#get new Rect
	sprite.rect = sprite.image.get_rect()
	#set new center to original center
	sprite.rect.center = oldCenter

def frame_generator(the_list):
	iterator = itertools.cycle(iter(the_list))
	while True:
		yield next(iterator)

class Bullet(pygame.sprite.Sprite):
	"""Constructor, creates a bullet fired by one of the two players."""

	def __init__(self):
		""" Constructor. Creates a bullet. Takes a
		preloaded image as imagetype. """
		super().__init__()
		self.origimage = pygame.image.load("bullets.png").convert_alpha()
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


class Game():
	"""Initializes the game and handles user input, loading, pausing etc..."""
	def __init__(self):
		# Initialize pygame
		pygame.init()
		# Naming the display surface
		self.screen = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
		# Setting the caption of window
		pygame.display.set_caption(CAPTION, 'Space')
		# Setting up sound
		pygame.mixer.init()
		# ----------- VARIOUS LOADING --------------------
		self.clock = pygame.time.Clock()
		self.background = pygame.image.load("space.png")

	def setup(self):
		# -------------------- 360 Controller Works --------------------------
		print('Setting up joystick...')
		self.joystick_count = pygame.joystick.get_count()
		if self.joystick_count == 0:
			print("Error, no joystick found!")
		else:
			for i in range(self.joystick_count):
				self.joystick = pygame.joystick.Joystick(i)
				self.joystick.init()
				self.joystick_name = self.joystick.get_name()
				print(self.joystick_name)
		
		self.all_sprites_list = pygame.sprite.Group()
		self.player = Player()
		self.all_sprites_list.add(self.player)

	def eventhandler(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		
		# Getting keyboard array:
		self.pressed = pygame.key.get_pressed()
		# Checking for keys and calling the wanted movement:
		# Quit:
		if self.pressed[pygame.K_ESCAPE]:
			exit()
		if self.pressed[pygame.K_a]:
			self.player.animate(self.screen)
		if self.pressed[pygame.K_RIGHT]:
			self.player.turnRight()
		if self.pressed[pygame.K_LEFT]:
			self.player.turnLeft()
		if self.pressed[pygame.K_UP]:
			self.player.thrusting = True
		if self.pressed[pygame.K_KP0]:
			self.player.fire()
		



	def run(self):
			"""Runs an instance of itself..."""
			self.setup()
			while True:
				while GAME_STATE:
					# Set background to space image
					self.screen.blit(self.background, (0, 0))
					# Handling events
					self.eventhandler()
					self.all_sprites_list.update()
					self.all_sprites_list.draw(self.screen)
					
					pygame.display.flip()
					# Limit to 60 frames per second
					self.clock.tick(FPS)

# ---------------------------------------------------
#                  MAIN PROGRAM LOOP 
# ---------------------------------------------------

if __name__ == "__main__":
	game = Game()
	game.run()