from settings import *
import pygame
from pygame.locals import *
import socket
from payload import *
import pickle

class BaseClient:
    """Represents the base class for a dumb client.  This client opens a socket connection to a server, sends
    game input updates to the server and receives game state from the server which is then drawn to the screen.

    BaseClient has the following data:
    host -- The server host.
    port -- The port the server is bound to.
    buffer_size -- The size of the socket buffer.
    socket -- The actual socket connection
    assets -- A dictionary storing all Actor textures.
    actors -- A dictionary storing all Actors.

    """

    def __init__(self):
        self.host = host
        self.port = port
        self.buffer_size = 10240
        """
        Create and open a socket connection to the server.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.assets = {}
        self.actors = {}

    def init_pygame(self):
        """Initializes and displays the pygame window with width, height values from settings.py

        """
        size   = [width, height]
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def __del__(self):
        """Close the socket connection on object destruction.

        """
        self.socket.close()

    def send(self, p):
        """Sends a payload to the server over the socket connection.

        Data:
        p -- An instance of a Payload object found in payload.py

        The payload object is serialized using the Python pickle module.  For more information on pickle see:
        1) http://docs.python.org/library/pickle.html
        2) http://wiki.python.org/moin/UsingPickle

        """
        data = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
        self.socket.send(data)

    def receive(self):
        """Receive data on the socket.  This function must be overridden by a class which inherits from BaseClient.

        """
        pass

    def draw_screen(self, game_state):
        """Draw the current game state on the screen.  This function must be overridden by a class which inherits from BaseClient.

        """
        pass

    def game_loop(self):
        """A basic game loop.

        Loop forever until the client closes the window.  Query the input state for up/down keys.  Put these button
        states into a payload packet and send them to the server, then wait for a response back.

        """
        done = False
        while not done:
            up, down = False, False
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    done = True
            if key[K_UP]:
                up = True
            if key[K_DOWN]:
                down = True
            input = {
                    'up' : up,
                    'down' : down,
                    'quit' : done
            }
            # Send input to server
            data = {'user_input' : input}
            payload = Payload(game_state, data)
            self.send(payload)

            # Receive gamestate update from the server
            state = self.receive()
            if state:
                self.draw_screen(state)
                pygame.time.delay(10)





