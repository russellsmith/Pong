from settings import *
import pygame
from pygame.locals import *
import socket
from payload import *
import pickle

class BaseClient:

    def __init__(self):
        self.host = host
        self.port = port
        self.buffer_size = 10240
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.assets = {}
        self.actors = {}

    def init_pygame(self):
        size   = [width, height]
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def __del__(self):
        self.socket.close()

    def send(self, p):
        data = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
        self.socket.send(data)

    def receive(self):
        # Receive data on the socket
        pass

    def draw_screen(self, game_state):
        pass

    def game_loop(self):
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





