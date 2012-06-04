from objectserver import *
from assetserver import *
from zipserver import *


"""
Change the following line to represent which type of server you're using.

One of the following should be used:

game = ObjectServer()
game = AssetServer()
game = ZipServer()
"""
server = ZipServer()
server.listen()