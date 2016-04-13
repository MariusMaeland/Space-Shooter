#!/usr/bin/env python3
import pygame
import random
import math
from config import *
from bullet import Bullet
from player import Player
from asteroid import Asteroid
from explosion import Explosion
from animation import Animation
from precode import *
from functions import *

"""
Space Shooter Game
Made by
Marius Maeland and Raymon Skjørten Hansen

Thanks to all the makers of the awesome sprites we have used!
See: references.txt 
"""

class Game():
	"""Initializes the game and handles setting up the game,
	user input, collision-checks and prints player info on the screen."""
	def __init__(self):
		# Initialize pygame
		pygame.init()
		# Naming the display surface
		self.screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
		# Setting the caption of window
		pygame.display.set_caption(CAPTION, 'Space')

		# ----------- VARIOUS LOADING --------------------
		self.clock = pygame.time.Clock()
		self.background = pygame.image.load("images/space.png")
		# Loading font
		self.font = pygame.font.SysFont('Roboto-Black.ttf', 25, False, False)

	def setup(self):
		"""Loads and cuts all the sprite sheets.
		Makes all instances of the needed objects and puts them in their 
		respective groups and lists

		Calling this method will effectively reset the game to it's initial state"""
		#-----------------------------------------------------------------------
		#                    SETTING UP EXPLOSION-SHEET
		#-----------------------------------------------------------------------
		self.explosion_image = pygame.image.load("images/exp2.png").convert_alpha()
		self.explosion_list = []
		self.esw = 900//9 # Finds the with of each frame used in the animation. esw = explosion sheet width
		for i in range(9): # Because there are 9 rows of images on the sheet
			for j in range(9):
				for n in range(2): # Add each of them frames twice to lengthen the animation.
					self.explosion_list.append(self.explosion_image.subsurface(j*self.esw, i*self.esw, self.esw, self.esw))

		#-----------------------------------------------------------------------
		#                    SETTING UP ASTEROID-SHEET
		#-----------------------------------------------------------------------
		self.asteroid_image = pygame.image.load("images/asteroids.png").convert_alpha()
		self.asteroid_list = []
		self.asw = 1024//8 # Divide by eight because there are eight images per row on the sheet. ESW = explosion sheet witdh.
		for i in range(4): # Because there are 4 rows of images on the sheet 
			for j in range(8):
				for n in range(3): # Add each frame 3 times to slow down the rotation
					self.asteroid_list.append(self.asteroid_image.subsurface(j*self.asw, i*self.asw, self.asw, self.asw))
		
		#-----------------------------------------------------------------------
		#                    SETTING UP FUEL, HEALTH and AMMO -SHEETS
		#-----------------------------------------------------------------------
		def sheetcutter(filename):
			"""Small function that cuts from the same sprite sheet."""
			cut_image = pygame.image.load(filename).convert_alpha()
			listing = []
			w = 1340//10
			for i in range(10):
				for n in range(3):
					listing.append(cut_image.subsurface(i*w, 0, w, 128))
			return listing

		self.fuel_list = sheetcutter("images/fuelsheet.png")
		self.health_list = sheetcutter("images/healthsheet.png")
		self.ammo_list = sheetcutter("images/ammosheet.png")

		#------------------------------------------------------------------------
		# 					SETTING UP DUST EXPLOSION
		#------------------------------------------------------------------------
		self.dust_sheet = pygame.image.load("images/dust_sheet.png").convert_alpha()
		# Uses a generic sprite sheet function
		self.dust_list = img_list(self.dust_sheet, 8, 3)

		#------------------------------------------------------------------------
		# 					SETTING UP GREEN HOLE
		#------------------------------------------------------------------------
		# Does not use the generic sprite sheet function, because it doesn't handle 
		# blank space between each frame in the sheet.
		self.hole_sheet = pygame.image.load("images/greenhole_sheet.png").convert_alpha()
		self.hole_list = []
		self.smbh = (self.hole_sheet.get_width()-90)//15
		for x in range(15):
			for f in range(2):
				self.hole_list.append(self.hole_sheet.subsurface(x*self.smbh+x*6, 0, self.smbh, self.smbh))

		#-----------------------------------------------------------------------
		#                    SETTING UP SPRITEGROUPS
		#-----------------------------------------------------------------------
		# One group to rule them all!!!
		self.all_sprites_list = pygame.sprite.Group()
		# One for each of the players bullets
		self.player1_bullets = pygame.sprite.Group()
		self.player2_bullets = pygame.sprite.Group()
		# One for each of the other elements in the game.
		self.fuel_group = pygame.sprite.Group()
		self.asteroid_group = pygame.sprite.Group()
		self.health_group = pygame.sprite.Group()
		self.ammo_group = pygame.sprite.Group()

		# Initializes the two players
		self.player1 = Player(P1STARTPOS, P1STARTANGLE)
		self.player2 = Player(P2STARTPOS, P2STARTANGLE)
		self.all_sprites_list.add(self.player1, self.player2)

		# Initializes the asteroids
		for i in range(ASTEROIDSNUM):
			size = random.randint(50, 100)
			self.asteroid = Asteroid(self.asteroid_list, size, size)
			self.all_sprites_list.add(self.asteroid)
			self.asteroid_group.add(self.asteroid)

		# Initalizes the fuel crystal
		for i in range(FUELNUM):
			self.fuel = Animation(self.fuel_list, (random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
												  (random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))),
												   44, 42)
			self.all_sprites_list.add(self.fuel)
			self.fuel_group.add(self.fuel)

		# Initializes the health crystal
		for i in range(HEALTHNUM):
			self.health = Animation(self.health_list, (random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
													  (random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))),
													   44, 42)
			self.all_sprites_list.add(self.health)
			self.health_group.add(self.health)

		# Initializes the ammo crystal
		for i in range(AMMONUM):
			self.ammo = Animation(self.ammo_list, (random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
												  (random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))),
												   44, 42)
			self.all_sprites_list.add(self.ammo)
			self.ammo_group.add(self.ammo)

		# Initalizes the green gravity hole
		self.blackhole = Animation(self.hole_list, SCREENWIDTH//2, SCREENHEIGHT//2, 100, 100)
		self.all_sprites_list.add(self.blackhole)
		

	def collisionchecks(self):
		"""Collision handler to handle all of the collision checks"""
		if DEBUG:
			pygame.draw.line(self.screen, RED, (SCREENWIDTH//2, 0), (SCREENWIDTH//2, SCREENHEIGHT),1 )
			pygame.draw.line(self.screen, RED, (0, SCREENHEIGHT//2), (SCREENWIDTH, SCREENHEIGHT//2), 1)
		#-----------------------------------------------------------------------
		#                    Player 2 gets hit or killed by player 1!
		#-----------------------------------------------------------------------
		for bullet in self.player1_bullets:
			if pygame.sprite.collide_mask(bullet, self.player2):
				if self.player2.invincible:
					pass
				elif self.player2.hp > 0:
					self.player2.hp -= bullet.damage
					self.hitpointexp = Explosion(self.explosion_list, bullet.rect.x, bullet.rect.y, 50, 50)
					self.all_sprites_list.add(self.hitpointexp)
					if self.player2.hp <= 0:
						self.player2.dead = True
						self.death = Explosion(self.explosion_list, self.player2.rect.centerx, self.player2.rect.centery, 200, 200)
						self.all_sprites_list.add(self.death)
						self.player2.squish(P2DEADPOS)
						self.player1.kills += 1
						self.player2.fuel = 100
				bullet.kill()
		#-----------------------------------------------------------------------
		#                    Player 1 gets hit or killed by player 2!
		#-----------------------------------------------------------------------
		for bullet in self.player2_bullets:
			if pygame.sprite.collide_mask(bullet, self.player1):
				if self.player1.invincible:
					pass
				elif self.player1.hp > 0:
					self.player1.hp -= bullet.damage
					self.hitpointexp = Explosion(self.explosion_list, bullet.rect.x, bullet.rect.y, 50, 50)
					self.all_sprites_list.add(self.hitpointexp)
					if self.player1.hp <= 0:
						self.player1.dead = True
						self.death = Explosion(self.explosion_list, self.player1.rect.centerx, self.player1.rect.centery, 200, 200)
						self.all_sprites_list.add(self.death)
						self.player1.squish(P1DEADPOS)
						self.player2.kills += 1
						self.player1.fuel = 100
					
				bullet.kill()
		#-----------------------------------------------------------------------
		#                    If the players crash!
		#-----------------------------------------------------------------------	
		if pygame.sprite.collide_mask(self.player1, self.player2):
			if (self.player1.dead or self.player2.dead):
				pass
			if (self.player1.invincible or self.player2.invincible):
				pass
			else:
				p1dir = (self.player1.pos - self.player2.pos)
				self.player1.speed += p1dir
				
				p2dir = (self.player2.pos - self.player1.pos)
				self.player2.speed += p2dir

				self.player1.hp -= 10 
				self.player2.hp -= 10
				if self.player1.hp <= 0:
					self.player1.dead = True
					self.supadeath1 = Explosion(self.explosion_list, self.player1.rect.centerx, self.player1.rect.centery, 400, 400)
					self.all_sprites_list.add(self.supadeath1)
					self.player1.squish(P1DEADPOS)
					self.player1.fuel = 100


				if self.player2.hp <= 0:
					self.player2.dead = True
					self.supadeath2 = Explosion(self.explosion_list, self.player2.rect.centerx, self.player2.rect.centery, 400, 400)
					self.all_sprites_list.add(self.supadeath2)
					self.player2.squish(P2DEADPOS)
					self.player2.fuel = 100
				
				

		#-----------------------------------------------------------------------
		#                  If players crash in asteroids!
		#-----------------------------------------------------------------------		

		# Player 1	
		for rock in self.asteroid_group:
			if pygame.sprite.collide_rect(self.player1, rock):
				if DEBUG:
					pygame.draw.rect(self.screen, (255,0,0), self.player1.rect, 1)
					pygame.draw.rect(self.screen, (255,0,255), rock.rect, 1)

				point = pygame.sprite.collide_mask(self.player1, rock)
				if point:
					if self.player1.invincible:
						pass
					else:
						self.player1.hp -= 20
						if self.player1.hp <= 0: 
							self.player1.dead = True 
							self.supadeath = Explosion(self.explosion_list, self.player1.rect.centerx, self.player1.rect.centery, 400, 400)
							self.all_sprites_list.add(self.supadeath)
							self.player1.squish(P1DEADPOS)
							self.player1.fuel = 100
							rock.respawn()
					dustexp = Explosion(self.dust_list, point[0]+self.player1.rect.x, point[1]+self.player1.rect.y, 50, 50)
					self.all_sprites_list.add(dustexp)

					pdir = (self.player1.pos - rock.pos)
					self.player1.speed += pdir
					
					adir = (rock.pos - self.player1.pos)
					rock.speed += adir	

			# Player 2
			if pygame.sprite.collide_rect(self.player2, rock):
				if DEBUG:
					pygame.draw.rect(self.screen, (255,0,0), self.player2.rect, 1)
					pygame.draw.rect(self.screen, (255,0,255), rock.rect, 1)
				point = pygame.sprite.collide_mask(self.player2, rock)
				if point:
					if self.player2.invincible:
						pass
					else:
						self.player2.hp -= 20
						if self.player2.hp <= 0:
							self.player2.dead = True
							self.supadeath = Explosion(self.explosion_list, self.player2.rect.centerx, self.player2.rect.centery, 400, 400)
							self.all_sprites_list.add(self.supadeath)
							self.player2.squish(P2DEADPOS)
							self.player2.fuel = 100
							rock.respawn()
					dustexp = Explosion(self.dust_list, point[0]+self.player2.rect.x, point[1]+self.player2.rect.y, 50, 50)
					self.all_sprites_list.add(dustexp)

					pdir = (self.player2.pos - rock.pos)
					self.player2.speed += pdir
				
					adir = (rock.pos - self.player2.pos)
					rock.speed += adir

		

		#-----------------------------------------------------------------------
		#      If the players get a fuel-crystal
		#-----------------------------------------------------------------------	
		
		for crystal in self.fuel_group:
			# Player 1
			if pygame.sprite.collide_mask(crystal, self.player1):
				self.player1.fuel = min(100, self.player1.hp + crystal.fuelamount)
				crystal.respawn((random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
								(random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))))

			# Player 2
			if pygame.sprite.collide_mask(crystal, self.player2):
			 	self.player2.fuel = min(100, self.player2.fuel + crystal.fuelamount)
			 	crystal.respawn((random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
								(random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))))
		
		#-----------------------------------------------------------------------
		#      If the players get a healing-crystal
		#-----------------------------------------------------------------------	
		
		for crystal in self.health_group:
			# Player 1
			if pygame.sprite.collide_mask(crystal, self.player1):
				self.player1.hp = min(100, self.player1.hp + crystal.hpamount)
				crystal.respawn((random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
								(random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))))

			# Player 2
			if pygame.sprite.collide_mask(crystal, self.player2):
			 	self.player2.hp = min(100, self.player2.hp + crystal.hpamount)
			 	crystal.respawn((random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
								(random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))))

		#--------------------------------------------------------a---------------
		#      If the players get a ammo-crystal
		#-----------------------------------------------------------------------	
		
		for crystal in self.ammo_group:
			# Player 1	
			if pygame.sprite.collide_mask(crystal, self.player1):
				self.player1.ammo = min(100, self.player1.ammo + crystal.ammoamount)
				crystal.respawn((random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
								(random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))))
				if (random.randint(1, 100) <= WEAPONUPCHANCE) and not self.player1.weaponup: 
					self.player1.weaponup = True
					self.player1.rate_of_fire = 200

			# Player 2
			if pygame.sprite.collide_mask(crystal, self.player2):
			 	self.player2.ammo = min(100, self.player2.ammo + crystal.ammoamount)
			 	crystal.respawn((random.randint((0+SCREENWIDTH//4),(SCREENWIDTH-SCREENWIDTH//4))), 
								(random.randint((0+SCREENHEIGHT//4),(SCREENHEIGHT-SCREENHEIGHT//4))))
			 	if (random.randint(1, 100) <= WEAPONUPCHANCE) and not self.player2.weaponup:
			 		self.player2.weaponup = True
			 		self.player2.rate_of_fire = 200

		#-----------------------------------------------------------------------
		#      If asteroids collide with asteroids
		#-----------------------------------------------------------------------
		
		for asteroid in self.asteroid_group:
			for rock in self.asteroid_group:
				if rock is not asteroid:
					if pygame.sprite.collide_rect(asteroid, rock):
						if DEBUG:
							pygame.draw.rect(self.screen, (255,0,0), asteroid.rect, 1)
							pygame.draw.rect(self.screen, (255,0,255), rock.rect, 1)

						point = pygame.sprite.collide_mask(asteroid, rock)
						if point:
							dustexp = Explosion(self.dust_list, point[0]+asteroid.rect.x, point[1]+asteroid.rect.y, 50, 50)
							self.all_sprites_list.add(dustexp)
							collision = (asteroid.pos - rock.pos).normalized() * (-1)
							asteroid.speed -= asteroid.speed.magnitude() * collision

		#-----------------------------------------------------------------------
		#      If asteroids gets shot
		#-----------------------------------------------------------------------
		
		for asteroid in self.asteroid_group:
			# Player 1 bullets againts asteroids
			for bullet in self.player1_bullets:
				if pygame.sprite.collide_rect(asteroid, bullet):
					point1 = pygame.sprite.collide_mask(asteroid, bullet)
					if point1:
						asteroid.hp -= 1
						self.hitpointexp = Explosion(self.explosion_list, bullet.rect.x, bullet.rect.y, 50, 50)
						self.all_sprites_list.add(self.hitpointexp)
						if asteroid.hp <= 0:
							self.supadeath = Explosion(self.explosion_list, asteroid.rect.centerx, asteroid.rect.centery, asteroid.width*2, asteroid.height*2)
							self.all_sprites_list.add(self.supadeath)
							asteroid.respawn()
						bullet.kill()

			# Player 2 bullets against asteroids
			for asteroid in self.asteroid_group:
				for bullet in self.player2_bullets:
					if pygame.sprite.collide_rect(asteroid, bullet):
						point2 = pygame.sprite.collide_mask(asteroid, bullet)
						if point2:	
							asteroid.hp -= 1
							self.hitpointexp = Explosion(self.explosion_list, bullet.rect.x, bullet.rect.y, asteroid.width, asteroid.height)
							self.all_sprites_list.add(self.hitpointexp)
							if asteroid.hp <= 0:
								self.supadeath = Explosion(self.explosion_list, asteroid.rect.centerx, asteroid.rect.centery, asteroid.width*2, asteroid.height*2)
								self.all_sprites_list.add(self.supadeath)
								asteroid.respawn()
							bullet.kill()

		#-----------------------------------------------------------------------
		#		PLAYERS REACH EVENT HORIZON!
		#-----------------------------------------------------------------------
		
		# Player 1
		if self.player1.direction.magnitude() < 25:
			self.player1.dead = True 
			self.player1.squish(P1DEADPOS)
		
		# Player 2
		if self.player2.direction.magnitude() < 25:
			self.player2.dead = True
			self.player2.squish(P2DEADPOS)

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
			if self.player2.fuel > 0:
				self.player2.thrusting = True
		if self.pressed[pygame.K_RCTRL]:
			self.player2.fire(self.all_sprites_list, self.player2_bullets)

		if self.pressed[pygame.K_d]:
			self.player1.turnRight()
		if self.pressed[pygame.K_a]:
			self.player1.turnLeft()
		if self.pressed[pygame.K_w]:
			if self.player1.fuel > 0:
				self.player1.thrusting = True
		if self.pressed[pygame.K_LSHIFT]:
			self.player1.fire(self.all_sprites_list, self.player1_bullets)

		if self.pressed[pygame.K_r]:
			self.setup()
			GAME_STATE = True

	def player_info(self):
		"""Setting up player information and blitting it on the screen"""
		
		# Loading font
		self.p1_ammo = self.font.render('Ammo: %d' % self.player1.ammo, True, WHITE)
		self.p2_ammo = self.font.render('Ammo: %d' % self.player2.ammo, True, WHITE)
		self.p1_stats = self.font.render('kills: %d' % self.player1.kills, True, WHITE)
		self.p2_stats = self.font.render('kills: %d' % self.player2.kills, True, WHITE)
		#player 1 stats and ammo info
		self.screen.blit(self.p1_stats, [10, 10])
		self.screen.blit(self.p1_ammo, [10, 30])
		#player 2 stats and ammo info
		self.screen.blit(self.p2_stats, [SCREENWIDTH - 105, 10])
		self.screen.blit(self.p2_ammo, [SCREENWIDTH - 105, 30])
		#Player 1 hp-bar:
		if self.player1.invincible:
			p1color = YELLOW
		else:
			p1color = RED
		pygame.draw.rect(self.screen, WHITE, (10, (SCREENHEIGHT-30), 202, 12), 1)
		pygame.draw.rect(self.screen, p1color, (11, (SCREENHEIGHT-29), (max(0,(self.player1.hp * 2))), 10))
		#Player 2 hp-bar
		if self.player2.invincible:
			p2color = YELLOW
		else:
			p2color = RED
		pygame.draw.rect(self.screen, WHITE, ((SCREENWIDTH-222), (SCREENHEIGHT-30), 202, 12), 1)
		pygame.draw.rect(self.screen, p2color, ((SCREENWIDTH-221), (SCREENHEIGHT-29), (max(0,(self.player2.hp * 2))), 10))
		#player 1 fuel bar
		pygame.draw.rect(self.screen, WHITE, (10, (SCREENHEIGHT-50), 202, 12), 1)
		pygame.draw.rect(self.screen, GREEN, (11, (SCREENHEIGHT-49), (self.player1.fuel * 2), 10))
		# Player 1 weaponupgrade-bar
		if self.player1.weaponup:
			fraction1 = 200//((FPS*WEAPONUPTIME)/self.player1.weaponup_tick)
			pygame.draw.rect(self.screen, WHITE, (10, (SCREENHEIGHT-80), 202, 12), 1)
			pygame.draw.rect(self.screen, LIGHTBLUE, (11, (SCREENHEIGHT-79), (200-fraction1), 10))
		#player 2 fuel bar
		pygame.draw.rect(self.screen, WHITE, ((SCREENWIDTH-222), (SCREENHEIGHT-50), 202, 12), 1)
		pygame.draw.rect(self.screen, GREEN, ((SCREENWIDTH-221), (SCREENHEIGHT-49), (self.player2.fuel * 2), 10))
		# Player 2 weaponupgrade-bar
		if self.player2.weaponup:
			fraction2 = 200//((FPS*WEAPONUPTIME)/self.player2.weaponup_tick)
			pygame.draw.rect(self.screen, WHITE, ((SCREENWIDTH-222), (SCREENHEIGHT-80), 202, 12), 1)
			pygame.draw.rect(self.screen, LIGHTBLUE, ((SCREENWIDTH-221), (SCREENHEIGHT-79), (200-fraction2), 10))


	def run(self):
			"""Runs an instance of itself..."""
			self.setup()
			while True:
				while GAME_STATE:
					# Set background to space image
					self.screen.blit(self.background, (0, 0))
					# Handling events
					self.eventhandler()
					self.all_sprites_list.update(self.screen, self.all_sprites_list)
					self.all_sprites_list.draw(self.screen)
					self.player_info()
					self.collisionchecks()
					pygame.display.flip()
					# Limit to 60 frames per second
					self.clock.tick(FPS)

# ---------------------------------------------------
#                  MAIN PROGRAM LOOP 
# ---------------------------------------------------

if __name__ == "__main__":
	game = Game()
	game.run()