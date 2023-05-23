from constants import TILE_SIZE


def getTileCoordinates(y, x):
    return (y + TILE_SIZE // 2) // TILE_SIZE, (x + TILE_SIZE // 2) // TILE_SIZE
