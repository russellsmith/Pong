import pickle
import pygame
import socket
from actor import *
from settings import *
from payload import *
from PIL import Image
import StringIO



class BaseServer:
    def __init__(self):
        size   = [width, height]

        paddle_image = Image.open('paddle.png')
        ball_image = Image.open('ball.png')
        paddle_buffer = paddle_image.convert("RGBA").tostring("raw", "RGBA")
        ball_buffer = ball_image.convert("RGBA").tostring("raw", "RGBA")


        paddle_rect = pygame.Rect(paddle_image.getbbox())
        paddle_rect2 = pygame.Rect(paddle_image.getbbox())
        ball_rect = pygame.Rect(ball_image.getbbox())
        #paddle_buffer = StringIO.StringIO()
        #paddle_image.rect = paddle_rect
        #ball_image.rect = ball_rect

        self.assets = {
            'paddle_image' : paddle_buffer,
            'ball_image' : ball_buffer
        }

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
        #paddle_rect = pygame.Rect(Image.fromstring('RGBA', self.assets['paddle_image'].len, self.assets['paddle_image']).getbbox())
        #ball_rect = pygame.Rect(Image.fromstring('RGBA', self.assets['ball_image'].len, self.assets['ball_image']).getbbox())
        #paddle_rect = self.assets['paddle_image'].rect
        #ball_rect = self.assets['ball_image'].rect

        ball = self.actors['ball']
        player1 = self.actors['player1']
        player2 = self.actors['player2']
        ball.x, ball.y, ball.xv, ball.yv = 25, 25, 5, 2
        player1.x, player1.y, player1.xv, player1.yv = 0, 0, 0, 0
        player2.x, player2.y, player2.xv, player2.yv = width - player2.rect.size[0], 0, 0, 0

        #self.actors['ball'] = Actor('ball_image', ball_rect, 25, 25, 5, 2)
        #self.actors['player1'] = Actor('paddle_image', paddle_rect, 0, 0, 0, 0)
        #self.actors['player2'] = Actor('paddle_image', paddle_rect, width - paddle_rect.size[0], 0, 0, 0)

    def send(self, p, connection):
        connection.send(p)

    def receive(self, packet, connection):
        # Receive data on the socket
        pass

    def listen(self):
        self.socket.listen(1)
        connection, address = self.socket.accept()
        print 'Connected to ', address
        while True:
            received = connection.recv(self.buffer_size)
            if received:
                p = pickle.loads(received)
                self.receive(p, connection)
            #connection.close()
            #print 'Connection closed with ', address

    def check_ball_collision(self, b, p):
        if(b.rect.colliderect(p.rect)):
            b.xv = -b.xv
            b.x += b.xv

    def check_ball_offscreen(self, b):
        if(b.rect.topleft[0] < 0):
            #ball left the screen
            self.reset_game()
            print 'offscreen1 reverse direction %d %d' % (b.xv, b.yv)
            return

        # Check to see if ball leaves the screen
        #print ball.rect.bottomright[1], ball.rect.topleft[1]
        if(b.rect.bottomright[1] > height or b.rect.topleft[1] < 0):
            b.yv = -b.yv
            b.y += b.yv
            print 'offscreen2 reverse direction %d %d' % (b.yv, b.y)
        if(b.rect.bottomright[0] > width or b.rect.topleft[0] < 0):
            b.xv = -b.xv
            b.x += b.xv
            print 'offscreen3 reverse direction %d %d' % (b.xv, b.x)

    def update_computer_position(self, b, p):
        # Get middle y value of paddle
        paddle_mid_y = p.rect.topleft[1] + (p.rect.bottomright[1] - p.rect.topleft[1]) / 2

        # Get middle y value of ball
        ball_mid_y = b.rect.topleft[1] + (b.rect.bottomright[1] - b.rect.topleft[1]) / 2
        #print computer_paddle.rect.topleft[1], computer_paddle.rect.bottomright[1], mid_y
        difference = abs(paddle_mid_y - ball_mid_y)
        difference = min(difference, 5)
        if paddle_mid_y > ball_mid_y:
            p.y += -difference
        else:
            p.y += difference

    def game_tick(self, user_input):
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
        #down, up = False, False

        if quit:
            #TODO quit!
            pass
        if up:
            paddle.y += paddle_velocity
        if down:
            paddle.y += -paddle_velocity

        paddle.rect.topleft = [0, paddle.y]
        paddle2.rect.topright = [width, paddle2.y]




