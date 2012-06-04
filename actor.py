class Actor:
    """Contains data relating to an Actor in the game.  For Pong, both paddles and the ball are actors.

    Has the following data:
    image -- the filename of the image which represents this Actor in the game (i.e. the texture name)
    rect -- the bounding rectangle for the Actor, used for collision detection
    x -- the x coordinate of the Actors current location.  This relates to the top left corner of its bounding rectangle.
    y -- the y coordinate of the Actors current location.  This relates to the top left corner of its bounding rectangle.
    xv -- the x portion of the Actors velocity vector.
    yv -- the y portion of the Actors velocity vector.

    """
    def __init__(self, image, rect, x, y, xv, yv):
        """Initialization of the Actors data."""
        self.image = image
        self.rect = rect
        self.rect.topleft = [x, y]
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv