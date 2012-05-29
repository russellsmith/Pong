#!/usr/bin/python
from objectclient import *

game = ObjectClient()
game.init_pygame()
game.game_loop()