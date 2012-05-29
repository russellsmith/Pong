#!/usr/bin/python
from objectclient import *
from assetclient import *
from zipclient import *

game = ZipClient()
game.init_pygame()
game.game_loop()