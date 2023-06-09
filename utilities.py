import pygame

from constants import TILE_SIZE
from enum import Enum


def getTileCoordinates(y, x):
    return (y + TILE_SIZE // 2) // TILE_SIZE, (x + TILE_SIZE // 2) // TILE_SIZE


def getFont(size):
    return pygame.font.Font(f"assets/font/font.ttf", size)


class Direction(Enum):
    UP = 'back'
    DOWN = 'front'
    LEFT = 'left'
    RIGHT = 'right'


class MoveState(Enum):
    STANDING = 'standing'
    RUNNING = 'running'


class MenuState(Enum):
    LOBBY = "lobby"
    MENU = "menu"
