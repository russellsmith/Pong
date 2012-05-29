from baseclient import *
import pickle

class ObjectClient(BaseClient):

    def receive(self):
        received = self.socket.recv(self.buffer_size)

        if received:
            game_state = pickle.loads(received)
            return game_state
        else:
            return None


    def draw_screen(self, game_state):
        ball = game_state.data['actors']['ball']
        paddle = game_state.data['actors']['player1']
        paddle2 = game_state.data['actors']['player2']

        ball_image = pygame.image.fromstring(game_state.data['assets'][ball.image], (ball.rect.width, ball.rect.height), 'RGBA')
        paddle_image = pygame.image.fromstring(game_state.data['assets'][paddle.image], (paddle.rect.width, paddle.rect.height), 'RGBA')
        paddle2_image = pygame.image.fromstring(game_state.data['assets'][paddle2.image], (paddle.rect.width, paddle.rect.height), 'RGBA')

        self.screen.fill([0, 0, 0])
        self.screen.blit(ball_image, ball.rect)
        self.screen.blit(paddle_image, paddle.rect)
        self.screen.blit(paddle2_image, paddle2.rect)

        pygame.display.update()
        print 'Drawing screen'