#!/usr/bin/python
from objectclient import *
from assetclient import *
from zipclient import *

"""
Change the following line to represent which type of client you're using.

One of the following should be used:

game = ObjectClient()
game = AssetClient()
game = ZipClient()
"""
game = ZipClient()
game.init_pygame()
game.game_loop()