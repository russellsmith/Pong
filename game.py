#!/usr/bin/python

import pygame
from pygame.locals import *

class Sprite:
    def __init__(self, image, rect, x, y, xv, yv):
        self.image = image
        self.rect = rect
        self.x = x
        self.y = y
        self.rect.topleft = [x, y]
        self.xv = xv
        self.yv = yv

class Socket:
    def __init__(self):
        # Open socket connection here
        pass

    def send(self):
        # Send data on the socket
        pass

    def receive(self):
        # Receive data on the socket
        pass

class Game:
    def __init__(self):
        pass

    def reset_game(self):

        b = Sprite(self.ball_image, self.ball_image.get_rect(), 25, 25, 5, 2)
        p = Sprite(self.paddle_image, self.paddle_image.get_rect(), 0, 0, 0, 0)
        p2 = Sprite(self.paddle_image, self.paddle_image.get_rect(), self.width - self.paddle_image.get_width(), 0, 0, 0)

        return b, p, p2

    def check_ball_collision(self, b, p):
        if(b.rect.colliderect(p.rect)):
            b.xv = -b.xv
            b.x += b.xv

    def check_ball_offscreen(self, b):
        if(b.rect.topleft[0] < 0):
            #ball left the screen
            self.ball, self.paddle, self.paddle2 = self.reset_game()
            print 'offscreen1 reverse direction %d %d' % (b.xv, b.yv)
            return

        # Check to see if ball leaves the screen
        #print ball.rect.bottomright[1], ball.rect.topleft[1]
        if(b.rect.bottomright[1] > self.height or b.rect.topleft[1] < 0):
            b.yv = -b.yv
            b.y += b.yv
            print 'offscreen2 reverse direction %d %d' % (b.yv, b.y)
        if(b.rect.bottomright[0] > self.width or b.rect.topleft[0] < 0):
            b.xv = -b.xv
            b.x += b.xv
            print 'offscreen3 reverse direction %d %d' % (b.xv, b.x)

    def update_computer_position(self, b, p):
        # Get middle of paddle

        paddle_mid_y = p.rect.topleft[1] + (p.rect.bottomright[1] - p.rect.topleft[1]) / 2
        ball_mid_y = b.rect.topleft[1] + (b.rect.bottomright[1] - b.rect.topleft[1]) / 2
        #print computer_paddle.rect.topleft[1], computer_paddle.rect.bottomright[1], mid_y
        difference = abs(paddle_mid_y - ball_mid_y)
        difference = min(difference, 5)
        if paddle_mid_y > ball_mid_y:
            p.y += -difference
        else:
            p.y += difference

    def game_loop(self):
        self.width  = 640
        self.height = 480
        size   = [self.width, self.height]
        pygame.init()
        screen = pygame.display.set_mode(size)
        background = pygame.Surface(screen.get_size())

        #paddle = pygame.sprite.Sprite() # create sprite
        self.paddle_image = pygame.image.load("paddle.png").convert_alpha() # load ball image

        #paddle2 = pygame.sprite.Sprite()
        #paddle2.image = paddle.image


        #ball = pygame.sprite.Sprite()
        self.ball_image = pygame.image.load("ball.png").convert_alpha()
        self.ball, self.paddle, self.paddle2 = self.reset_game()
        screen.blit(self.ball.image, self.ball.rect)
        screen.blit(self.paddle.image, self.paddle.rect)
        screen.blit(self.paddle2.image, self.paddle2.rect)



        #ypos = 0
        pygame.display.update()
        done = False
        while not done:
            # Update ball position
            self.ball.x += self.ball.xv
            self.ball.y += self.ball.yv
            self.ball.rect.topleft = [self.ball.x, self.ball.y]
            self.check_ball_offscreen(self.ball)
            self.check_ball_collision(self.ball, self.paddle)
            self.check_ball_collision(self.ball, self.paddle2)
            self.update_computer_position(self.ball, self.paddle2)
            #down, up = False, False
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    done = True
            if key[K_UP]:
                self.paddle.y += -5
            if key[K_DOWN]:
                self.paddle.y += 5

            self.paddle.rect.topleft = [0, self.paddle.y]
            self.paddle2.rect.topright = [self.width, self.paddle2.y]
            screen.fill([0, 0, 0])
            screen.blit(self.ball.image, self.ball.rect)
            screen.blit(self.paddle.image, self.paddle.rect)
            screen.blit(self.paddle2.image, self.paddle2.rect)

            pygame.display.update()
            pygame.time.delay(30)

g = Game()
g.game_loop()