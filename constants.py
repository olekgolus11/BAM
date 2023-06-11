import math

FPS = 60
PORT = 3000

BOARD_WIDTH = 21
BOARD_HEIGHT = 11


FIRST_BOMB_STATE = 40
SECOND_BOMB_STATE = 80
THIRD_BOMB_STATE = 120
FOURTH_BOMB_STATE = 160

BOMB_IMAGE_1 = 'assets/bomb/bomb1.png'
BOMB_IMAGE_2 = 'assets/bomb/bomb2.png'
BOMB_IMAGE_3 = 'assets/bomb/bomb3.png'
FIRE_IMAGE = 'assets/bomb/fire.png'

FLOOR = 0
CRATE = 1.0
MORE_BOMBS = 3.0
MORE_POWER = 4.0
MORE_SPEED = 5.0
WALL = 8.0
TOP_WALL = 9.0


TILE_SIZE = 60

CIRCLE_RADIUS = 60
CIRCLE_Y_POS = 360
MENU_TEXT_FONT_SIZE = 75

PLAYER_FONT_SIZE = 18
PLAYER_TEXT_Y_POS = 275

PLAYER_ONE_X_POS = 240
PLAYER_TWO_X_POS = 640
PLAYER_THREE_X_POS = 1040


CENTER_X_POS = 640
CENTER_Y_POS = 360
AVATAR_PADDING = 30

LOBBY_PLAYER_IMAGE_1 = f"assets/player/char1_front_standing.png"
LOBBY_PLAYER_IMAGE_2 = f"assets/player/char2_front_standing.png"
LOBBY_PLAYER_IMAGE_3 = f"assets/player/char3_front_standing.png"

RULES_RECTANGLE_HEIGHT = 500
RULES_RECTANGLE_WIDTH = 1150
COUNTER_Y_POS = 550
JOIN_BACK_BUTTON_Y_POS = 640

TEXTFIELD_WIDTH = 300
TEXTFIELD_HEIGHT = 50
TEXTFIELD_Y_POS = 305

ROUNDS_TO_WIN_GAME = 5
SECONDS_TO_START_GAME = 5
RESET_ROUND_TIME = 2

PLAYER_1_Y_POS = 60
PLAYER_1_X_POS = 60

PLAYER_2_Y_POS = 60
PLAYER_2_X_POS = BOARD_WIDTH * TILE_SIZE - 120

PLAYER_3_Y_POS = BOARD_HEIGHT * TILE_SIZE - 120
PLAYER_3_X_POS = 60
