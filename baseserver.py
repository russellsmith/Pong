import pickle
import pygame
import socket
from actor import *
from settings import *
from payload import *
from PIL import Image
import StringIO



class BaseServer:
    """Represents the base class for a pong server.  Stores assets and actors in separate dictionary objects.  Handles
    all game logic.

    Data:
    assets -- A dictionary containing Actor textures.
    actors -- A dictionary containing Actor.
    host -- The host the server is running on.
    port -- The port the server is running on.
    buffer_size -- The buffer size of the socket connection.
    socket -- The actual socket connection.

    """
    def __init__(self):
        """Initialize the state of the server.  Load all assets, instantiate Actors in their default states, and open a
        socket for listening for a connection on.

        """

        # Client window size loaded from settings.py
        size   = [width, height]

        # Load all art assets using PIL.
        paddle_image = Image.open('paddle.png')
        ball_image = Image.open('ball.png')

        # Convert all images to raw strings ready to be sent over a socket connection.
        paddle_buffer = paddle_image.convert("RGBA").tostring("raw", "RGBA")
        ball_buffer = ball_image.convert("RGBA").tostring("raw", "RGBA")

        # Store assets
        self.assets = {
            'paddle_image' : paddle_buffer,
            'ball_image' : ball_buffer
        }

        # Calculate pygame Rect objects for all Actors
        paddle_rect = pygame.Rect(paddle_image.getbbox())
        paddle_rect2 = pygame.Rect(paddle_image.getbbox())
        ball_rect = pygame.Rect(ball_image.getbbox())


        # Instantiate and store Actor objects.
        b = Actor('ball_image', ball_rect, 25, 25, 5, 2)
        p = Actor('paddle_image', paddle_rect, 0, 0, 0, 0)
        p2 = Actor('paddle_image', paddle_rect2, width - paddle_rect.size[0], 0, 0, 0)
        self.actors = {
            'ball' : b,
            'player1' : p,
            'player2' : p2
        }
        self.host = host
        self.port = port
        self.buffer_size = 10240

        # Open the socket connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def __del__(self):
        # Close the socket connection
        self.socket.close()



    def reset_game(self):
        """Resets the game to its default state.  Occurs when the ball passes a paddle and leaves the screen.

        """

        ball = self.actors['ball']
        player1 = self.actors['player1']
        player2 = self.actors['player2']
        ball.x, ball.y, ball.xv, ball.yv = 25, 25, 5, 2
        player1.x, player1.y, player1.xv, player1.yv = 0, 0, 0, 0
        player2.x, player2.y, player2.xv, player2.yv = width - player2.rect.size[0], 0, 0, 0

    def send(self, p, connection):
        """Send a packet of information over a connection to a client

        """
        connection.send(p)

    def receive(self, packet, connection):
        """ Receives data over a connection to a client.  This function must be overridden by any classes that inherit
        from BaseServer.

        """
        pass

    def listen(self):
        """Listens for clients trying to connect to the server.

        """
        print 'Listening for incoming connections...'
        self.socket.listen(1)
        connection, address = self.socket.accept()
        print 'Connected to ', address
        while True:
            received = connection.recv(self.buffer_size)
            if received:
                p = pickle.loads(received)
                self.receive(p, connection)

    def check_ball_collision(self, b, p):
        """Checks for collision between a ball and a paddle.  If collision occurs reverse the x velocity of the ball.

        """
        if(b.rect.colliderect(p.rect)):
            b.xv = -b.xv
            b.x += b.xv

    def check_ball_offscreen(self, b):
        """Checks if the ball left the screen.  If it left the left or right edges of the screen, reset the game state.
        If it left the top or bottom edges of the screen, reverse the y direction of the ball.
        """
        if(b.rect.topleft[0] < 0 or b.rect.bottomright[0] > width):
            #ball left the screen
            self.reset_game()
            return

        # Check to see if ball leaves top or bottom edge of the screen
        if(b.rect.bottomright[1] > height or b.rect.topleft[1] < 0):
            b.yv = -b.yv
            b.y += b.yv
        if(b.rect.bottomright[0] > width or b.rect.topleft[0] < 0):
            b.xv = -b.xv
            b.x += b.xv

    def update_computer_position(self, b, p):
        """Update the computer paddle position based on the position of the ball.

        """
        # Get middle y value of paddle
        paddle_mid_y = p.rect.topleft[1] + (p.rect.bottomright[1] - p.rect.topleft[1]) / 2

        # Get middle y value of ball
        ball_mid_y = b.rect.topleft[1] + (b.rect.bottomright[1] - b.rect.topleft[1]) / 2
        difference = abs(paddle_mid_y - ball_mid_y)

        # clamp the velocity of the paddle at 5
        difference = min(difference, 5)

        # move the paddle
        if paddle_mid_y > ball_mid_y:
            p.y += -difference
        else:
            p.y += difference

    def game_tick(self, user_input):
        """Receives the user input state and updates the game state accordingly.

        """
        # Update ball position
        ball = self.actors['ball'];
        paddle = self.actors['player1']
        paddle2 = self.actors['player2']
        ball.x += ball.xv
        ball.y += ball.yv
        ball.rect.topleft = [ball.x, ball.y]
        self.check_ball_offscreen(ball)
        self.check_ball_collision(ball, paddle)
        self.check_ball_collision(ball, paddle2)
        self.update_computer_position(ball, paddle2)

        down, up, quit = user_input['up'], user_input['down'], user_input['quit']

        if quit:
            #TODO quit!
            pass
        if up:
            paddle.y += paddle_velocity
        if down:
            paddle.y += -paddle_velocity

        paddle.rect.topleft = [0, paddle.y]
        paddle2.rect.topright = [width, paddle2.y]




