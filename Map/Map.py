class Map:
    SQUARE_SIZE = 60
    WIDTH = 21
    HEIGHT = 11

    # 0.0 - floor
    # 1.0 - crate
    # 3.0 - more bombs
    # 4.0 - more power
    # 5.0 - more speed
    # 8.0 - wall
    # 9.0 - top wall

    board = [[9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 9.0],
             [9.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 9.0],
             [9.0, 0.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 0.0, 9.0],
             [9.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 9.0],
             [9.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 9.0],
             [9.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 9.0],
             [9.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 9.0],
             [9.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 9.0],
             [9.0, 0.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 1.0, 8.0, 0.0, 9.0],
             [9.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 9.0],
             [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0]]
