"""
config.py 
by member 4
"""
# screen configration
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
NUM_LANES = 4

# player configration
PLAYER_SIZE = 60
PLAYER_Y_RATIO = 0.85   # car locate
SMOOTHING = 0.25        #speed of switching between tracks

# obstacles and powerup config
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 40
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30

# game speed control
GAME_SPEED = 4           # speed of falling obstacle
SPAWN_INTERVAL = 20      # close proximity of obstacle and power up
BOOST_DURATION = 1.5     # boost intrval
# number of lives at the beginning
INITIAL_LIVES = 5