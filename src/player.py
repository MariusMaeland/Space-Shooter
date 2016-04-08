import pygame
from bullet import Bullet
import math
import random
from variables import *
from precode import * 

class Player(pygame.sprite.Sprite):

	def __init__(self, startpos, start_angle):
		""" Constructor. Creates a player. """
		super().__init__()
		# Set the starting image
		self.scale = 50
		self.origimage = pygame.transform.scale(pygame.image.load(random.choice(ship_image_list)), (self.scale, self.scale))
		self.image = self.origimage.copy()
		self.startx = startpos[0]
		self.starty = startpos[1]
		self.rect = self.image.get_rect()
		self.pos = Vector2D(self.startx, self.starty)
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y
		# Load the image for the thruster-flame
		self.thrusterimage = pygame.image.load("images/jetflame.png").convert_alpha()
		self.shieldimage = pygame.image.load("images/shieldsheet.png").convert_alpha()
		self.thruster = []
		self.shield = []
		 # Calculating how many pixels to cut each time from the sheet.
		self.thruster_width = 1920//30
		# Sprite number from the thruster list.
		self.nr = 0
		self.shieldnr = 0
		# Cut from the spritesheet and add them to the thruster-list.
		for i in range(30):
			self.thruster.append(self.thrusterimage.subsurface((i*self.thruster_width, 0, self.thruster_width, self.thruster_width)))
		for x in range(18):
			self.shield.append(self.shieldimage.subsurface((x*133, 0, 133, 133)))
		# Various attributes
		self.startdir = start_angle
		self.dir = start_angle
		self.speed = Vector2D(0,0)
		self.thrusting = False
		# Various ammo-related stuff
		self.ammo = 100
	
		self.last_shot = 0
		self.rate_of_fire = 100
		# Health-problems
		self.dead = False
		self.invincible = False
		self.invincible_tick = 0
		self.hp = 100
		self.respawn_tick = 0

		self.kills = 0
		self.fuel = 100
		self.vel = 0

		self.direction = BLACKHOLEPOS-self.pos

	def squish(self, deadpos):
		self.pos.x = deadpos[0]
		self.pos.y = deadpos[1]
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y
		self.vel = 0
		self.thrusting = False

	def thrust(self):
		"""Sets the thrust attribute to True and limits the speed"""
		if self.thrusting:
			if self.fuel > 0:
				# Makes the ship accelerate instead of instant getting top speed
				self.fuel -= 0.2
				self.vel = min(7, self.vel+1)

			self.thrusting = False


	def fire(self, all_sprites_list, bullet_list):
		"""Fires a shot, takes in all_sprites_list to get access to the group
		Firing is limited by the self.rate of fire(compulsory time in milliseconds
		between each shot). """
		if self.dead:
			pass
		else:
			# Restrain the rate of fire
			if (pygame.time.get_ticks()-self.last_shot) > (self.rate_of_fire):
				if self.ammo:
					bullet = Bullet()
					#game.lasersound.play()
					bullet.rect.centerx = self.rect.centerx
					bullet.rect.centery = self.rect.centery
					# Calculate vectors:
					bullet.xspeed = math.cos(math.radians(self.dir)) * 10
					bullet.yspeed = math.sin(math.radians(self.dir)) * -10
		        	# Add the bullets to the lists
					all_sprites_list.add(bullet)
					bullet_list.add(bullet)
					self.last_shot = pygame.time.get_ticks()
					# Decrease the ammo count
					self.ammo -= 1


	def turnLeft(self):
		"""Turns the ship to the left"""
		# How many degrees the ship turns left.
		self.dir += 4
		self.dir %= 360

	def turnRight(self):
		"""Turns the ship to the right"""
		# How many degrees the ship turns right.
		self.dir -= 4
		self.dir %= 360

	def update(self, screen, all_sprites_list):
		if self.dead:
			self.respawn_tick += 1
			if self.respawn_tick > (FPS * 3):
				self.respawn_tick = 0
				self.dead = False
				self.pos.x = self.startx 
				self.pos.y = self.starty
				self.rect.centerx = self.pos.x
				self.rect.centery = self.pos.y
				self.direction = BLACKHOLEPOS-self.pos
				self.vel = 0
				self.speed.x = 0
				self.speed.y = 0
				self.hp = 100
				self.fuel = 100
				self.dir = self.startdir
				self.invincible = True
		else:
			if self.invincible:
				self.invincible_tick += 1
				if self.invincible_tick > (FPS * 4):
					self.invincible = False
					self.invincible_tick = 0
			self.rotate_sprite(self.dir)
			self.thrust()

			self.speed.x += math.cos(math.radians(self.dir)) * self.vel
			self.speed.y -= math.sin(math.radians(self.dir)) * self.vel
			# Makes the ship gradually loose speed when not thrusting.
			self.vel = max(0, self.vel-0.2)
			
			#self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
			#self.rect.centery -= math.sin(math.radians(self.dir)) * self.speed
			# Limit the speed-vector
			if self.speed.magnitude() > PLAYERMAXSPEED:
				self.speed = self.speed.normalized() * PLAYERMAXSPEED
			else:
				self.speed *= 0.5
			self.pos += self.speed
			
			self.direction = BLACKHOLEPOS-self.pos
			
			self.speed += self.direction.normalized()*GRAVITY/self.direction.magnitude()
			#print(self.pos)
			
			self.rect.centerx = self.pos.x
			self.rect.centery = self.pos.y
			#---------------------------------------------
			#  				APPLYING GRAVITY
			#---------------------------------------------


	def rotate_sprite(sprite, degrees):
		"""Rotating the image and rect"""
		surfsize = (sprite.thruster[0].get_width() + sprite.scale//2)*2
		#get original center because new Rect center will change with image transformation.
		oldCenter = sprite.rect.center
		flamey_ship = pygame.Surface((surfsize, surfsize))
		ship_mask = flamey_ship.copy()
		#pygame.draw.rect(flamey_ship, (255,0,0), flamey_ship.get_rect(), 1)
		if sprite.thrusting:
			flamey_ship.blit(sprite.thruster[sprite.nr], (surfsize//2-sprite.scale//2-sprite.thruster[0].get_width(), 
														  surfsize//2-sprite.thruster[0].get_height()//2))
		sprite.nr += 1
		sprite.nr %= 30
		flamey_ship.blit(sprite.origimage, (surfsize//2-sprite.scale//2,surfsize//2-sprite.scale//2))
		ship_mask.blit(sprite.origimage, (surfsize//2-sprite.scale//2,surfsize//2-sprite.scale//2))
		if sprite.invincible:
			#flamey_ship.blit(sprite.shield[sprite.shieldnr], (29,35))
			pass
		sprite.shieldnr += 1
		sprite.shieldnr %= 18
		flamey_ship.set_colorkey((0,0,0))
		ship_mask.set_colorkey((0,0,0))
		#use pygame.transform.rotate(<image_to_rotate>, <turn_degrees>)
		sprite.image = pygame.transform.rotate(flamey_ship, degrees)
		sprite.mask = pygame.mask.from_surface(pygame.transform.rotate(ship_mask, degrees))
		#outline = sprite.mask.outline()
		#pygame.draw.lines(sprite.image, (255, 255, 0), 1, outline)
		#get new Rect
		sprite.rect = sprite.image.get_rect()
		#set new center to original center
		sprite.rect.center = oldCenter
