class Actor:
    def __init__(self, image, rect, x, y, xv, yv):
        self.image = image
        self.rect = rect
        self.x = x
        self.y = y
        self.rect.topleft = [x, y]
        self.xv = xv
        self.yv = yv