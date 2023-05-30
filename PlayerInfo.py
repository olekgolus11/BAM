class PlayerInfo:
    x = None
    y = None
    id = None

    def __init__(self, x, y, id, channel, imagePath):
        self.x = x
        self.y = y
        self.id = id
        self.imagePath = imagePath
        self.channel = channel
