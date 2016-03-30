import pygame
import math

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