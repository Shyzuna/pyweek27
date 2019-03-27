import os
import math

# Generation
MAP_MIN_DIST_PLAYER_EXIT = 10
MONSTERS_NUM = 10
MIN_DIST_PLAYER_MONSTERS = 3

# Display
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800
FPS = 60
AUTO_SIZE = True

# Paths
HEX_PATH = os.path.join('data', 'hex')
FONT_PATH = os.path.join('data', 'fonts')

# Map parameters
TILE_SIDE = 50
TILE_WIDTH = TILE_SIDE*2
TILE_HEIGHT = int(TILE_SIDE*math.sqrt(3))
TILES_NUM_WIDTH = 10
TILES_NUM_HEIGHT = 10

BORDER_TILES_NUM = 3
BORDER_TILES_WIDTH = TILE_WIDTH * BORDER_TILES_NUM
BORDER_TILES_HEIGHT = TILE_HEIGHT * BORDER_TILES_NUM

MAP_WIDTH = TILE_WIDTH * TILES_NUM_WIDTH + BORDER_TILES_WIDTH * 2
MAP_HEIGHT = TILE_HEIGHT * TILES_NUM_HEIGHT + BORDER_TILES_HEIGHT * 2
RECT_MAX_X = MAP_WIDTH - SCREEN_WIDTH
RECT_MAX_Y = MAP_HEIGHT - SCREEN_HEIGHT

# Scroll parameters
SCROLL_SPEED_HORIZONTAL = 1.0
SCROLL_SPEED_VERTICAL = 1.0
SCROLL_MOUSE_MARGIN = 5
SCROLL_MOUSE_MAX_X = SCREEN_WIDTH - SCROLL_MOUSE_MARGIN
SCROLL_MOUSE_MAX_Y = SCREEN_HEIGHT - SCROLL_MOUSE_MARGIN
