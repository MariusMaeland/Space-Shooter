# Space-Shooter

Requires Python 3
Requires pygame for python3

To run in terminal:

<python3 game.py>

-----------
HOW TO PLAY
----------
The Space Shooter pits two space ships against one another on a fixed screen.
Each player starts on his side of the screen. 
The object is simply to get more kills than your opponent.
The game does not end as such, but simply runs until you have crushed your opponent into submission.

Each player has 100 health points (RED BAR)
Each player has 100 bullets (uppper corner)
Each player has 100 units of fuel (GREEN BAR)

I fixed number of asteroids of various size will spawn off screen
and the be pulled in towards the center.
There is a black... green hole in the middle of the screen which pulls on everything except
bullets. 
Moving uses fuel. If run out, you will be pulled into the hole. Don't run out!

Getting hit by an asteroid will loose you 20 hp!
Asteroids will stop bullets but are destroyed after three hits.

If your hp reaches 0, you die(obviously).
After you respawn, you will have a 4 second period in which you are invincible.
During this period you hp- bar is yeallow

Both fuel, health and ammo can be refilled by grabbing the various crystals around the black hole.

RED crystals - grants 10 to 60 hp.
GREEN crystals - grants 30 to 60 fuel.
BLUE crystals - grants 20 bullets.

------------
CONFIG
-----------
Several of the variables used to shape the gameplay can be tweaked in the config.py file.
GRAVITY - Somewhere between 50 and 300 is managable
TIMETORESPAWN - Time in seconds to respawn
INVINCIBLETIME - Duration of invincible time in seconds
BULLETSPEED - Bullet speed in pixels/frame. 10 - 20 seems good.
PLAYERMAXSPEED - Speed in pixel/frame. 4-5 is good.
ASTEROIDSNUM - Number of asteroids (How long can you survive 40?!) 	
ASTEROIDSMAXSPEED - Maximum speed of asteroids
ASTEROIDSMINSPEED - Minimum speed of asteroids
FUELNUM - Number of green fuel-crystals
HEALTHNUM - Number of red health-crystals
AMMONUM - Number of blue ammo-crystals

------------
CONTROLS
------------
PLAYER 1:
Thrust: 	W
Rotate right: 	D
Rotate left: 	A
Fire: 		Left Shift

PLAYER 2:
Thrust:		UP
Rotate right:	RIGHT
Rotate left:	LEFT
Fire:		Right Ctr

Reset the game:	R

Exit/Close:	Esc
