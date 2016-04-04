#!/usr/bin/env python3
import pygame
import random
import math
from variables import *
from bullet import Bullet
from player import Player
from explosion import Explosion

class Game():
	"""Initializes the game and handles user input, loading, pausing etc..."""
	def __init__(self):
		# Initialize pygame
		pygame.init()
		# Naming the display surface
		self.screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT), pygame.FULLSCREEN, 32)
		# Setting the caption of window
		pygame.display.set_caption(CAPTION, 'Space')
		# Setting up sound
		pygame.mixer.init()
		# ----------- VARIOUS LOADING --------------------
		self.clock = pygame.time.Clock()
		self.background = pygame.image.load("images/space.png")
		# Loading font
		self.font = pygame.font.SysFont('fonts/Roboto-Black.ttf', 20, False, False)

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
		
		#-----------------------------------------------------------------------
		#                    SETTING UP EXPLOSION-SHEET
		#-----------------------------------------------------------------------
		self.explosion_image = pygame.image.load("images/exp2.png").convert_alpha()
		self.explosion_list = []
		self.esw = 900//9 # Divide by eight because there are eight images per row on the sheet. ESW = explosion sheet witdh.
		for i in range(9): # Because there are 8 rows of images on the sheet 
			for j in range(9):
				for n in range(2):
					self.explosion_list.append(self.explosion_image.subsurface(j*self.esw, i*self.esw, self.esw, self.esw))

		print(len(self.explosion_list))

		#-----------------------------------------------------------------------
		#                    SETTING UP SPRITEGROUPS
		#-----------------------------------------------------------------------
		self.all_sprites_list = pygame.sprite.Group()
		self.player1_bullets = pygame.sprite.Group()
		self.player2_bullets = pygame.sprite.Group()
		self.fuel_list = pygame.sprite.Group()
		self.asteroid_list = pygame.sprite.Group()

		self.player1 = Player(P1STARTPOS, P1STARTANGLE)
		self.player2 = Player(P2STARTPOS, P2STARTANGLE)
		self.all_sprites_list.add(self.player1)
		self.all_sprites_list.add(self.player2)
		
		#self.death = Explosion(self.explosion_list, 600, 350, 500, 500)
		#self.all_sprites_list.add(self.death)

	def collisionchecks(self):
		#-----------------------------------------------------------------------
		#                    Player 2 gets hit or killed!
		#-----------------------------------------------------------------------
		for bullet in self.player1_bullets:
			if pygame.sprite.collide_mask(bullet, self.player2):
				if self.player2.hp > 0:
					self.player2.hp -= 10
					self.hitpointexp = Explosion(self.explosion_list, bullet.rect.x, bullet.rect.y, 50, 50)
					self.all_sprites_list.add(self.hitpointexp)
					if self.player2.hp == 0:
						self.player2.dead = True
						self.death = Explosion(self.explosion_list, self.player2.rect.centerx, self.player2.rect.centery, 200, 200)
						self.all_sprites_list.add(self.death)
						self.player2.squish(P2DEADPOS)
				bullet.kill()
		#-----------------------------------------------------------------------
		#                    Player 1 gets hit or killed!
		#-----------------------------------------------------------------------
		for bullet in self.player2_bullets:
			if pygame.sprite.collide_mask(bullet, self.player1):
				if self.player1.hp > 0:
					self.player1.hp -= 10
					self.hitpointexp = Explosion(self.explosion_list, bullet.rect.x, bullet.rect.y, 50, 50)
					self.all_sprites_list.add(self.hitpointexp)
					if self.player1.hp == 0:
						self.player1.dead = True
						self.death = Explosion(self.explosion_list, self.player1.rect.centerx, self.player1.rect.centery, 200, 200)
						self.all_sprites_list.add(self.death)
						self.player1.squish(P1DEADPOS)
					
				bullet.kill()
		#-----------------------------------------------------------------------
		#                    If the player collides!
		#-----------------------------------------------------------------------	
		if pygame.sprite.collide_mask(self.player1, self.player2):
			if (self.player1.dead or self.player2.dead):
				pass
			else:
				self.player1.hp = 0 
				self.player2.hp = 0
				self.player1.dead = True 
				self.player2.dead = True
				self.supadeath = Explosion(self.explosion_list, self.player1.rect.centerx, self.player1.rect.centery, 400, 400)
				self.all_sprites_list.add(self.supadeath)
				self.player1.squish(P1DEADPOS)
				self.player2.squish(P2DEADPOS)
				#self.setup()

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
		if self.pressed[pygame.K_RIGHT]:
			self.player2.turnRight()
		if self.pressed[pygame.K_LEFT]:
			self.player2.turnLeft()
		if self.pressed[pygame.K_UP]:
			self.player2.thrusting = True
		if self.pressed[pygame.K_KP0]:
			self.player2.fire(self.all_sprites_list, self.player2_bullets)

		if self.pressed[pygame.K_d]:
			self.player1.turnRight()
		if self.pressed[pygame.K_a]:
			self.player1.turnLeft()
		if self.pressed[pygame.K_w]:
			self.player1.thrusting = True
		if self.pressed[pygame.K_q]:
			self.player1.fire(self.all_sprites_list, self.player1_bullets)

	def player_info(self):
		"""Setting up player information and blitting it on the screen"""

		p1_ammo = self.font.render('Ammo: %d' % self.player1.ammo, True, WHITE)
		p2_ammo = self.font.render('Ammo: %d' % self.player2.ammo, True, WHITE)

		self.screen.blit(p1_ammo, [10, 10])
		self.screen.blit(p2_ammo, [SCREENWIDTH - 105, 10])
		#Player 1 hp-bar:
		pygame.draw.rect(self.screen, WHITE, (10, (SCREENHEIGHT-30), 202, 12), 1)
		pygame.draw.rect(self.screen, RED, (11, (SCREENHEIGHT-29), (self.player1.hp * 2), 10))
		#Player 2 hp-bar
		pygame.draw.rect(self.screen, WHITE, ((SCREENWIDTH-222), (SCREENHEIGHT-30), 202, 12), 1)
		pygame.draw.rect(self.screen, RED, ((SCREENWIDTH-221), (SCREENHEIGHT-29), (self.player2.hp * 2), 10))
		
	def run(self):
			"""Runs an instance of itself..."""
			self.setup()
			while True:
				while GAME_STATE:
					#print("andre var her")
					# Set background to space image
					self.screen.blit(self.background, (0, 0))
					# Handling events
					self.eventhandler()
					self.all_sprites_list.update(self.screen, self.all_sprites_list)
					self.all_sprites_list.draw(self.screen)
					self.player_info()
					self.collisionchecks()
					print(self.all_sprites_list)
					pygame.display.flip()
					# Limit to 60 frames per second
					self.clock.tick(FPS)

# ---------------------------------------------------
#                  MAIN PROGRAM LOOP 
# ---------------------------------------------------

if __name__ == "__main__":
	game = Game()
	game.run()