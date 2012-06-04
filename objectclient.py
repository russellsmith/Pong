from baseclient import *
import pickle

class ObjectClient(BaseClient):
    """A type of client that expects the server to send the current game state along with all assets each
    frame.

    Actors data is expected to be in a dictionary with key name 'actors'.  This dictionary should have Actor objects
    'ball', 'player1', and 'player2' representing the ball, the player and the computer player respectively.

    Assets data is expected to be in a dictionary with key name 'assets'.

    """

    def receive(self):
        """Receives data, if any, sent over the socket and unpickles and returns it.  This function is called in
        game_loop of BaseClient.

        """
        received = self.socket.recv(self.buffer_size)

        if received:
            game_state = pickle.loads(received)
            return game_state
        else:
            return None


    def draw_screen(self, game_state):
        """Draws the screen based on the game state sent from the server.

        """
        # Get reference to the Actors
        ball = game_state.data['actors']['ball']
        paddle = game_state.data['actors']['player1']
        paddle2 = game_state.data['actors']['player2']

        # Convert PIL image strings to pygame images
        ball_image = pygame.image.fromstring(game_state.data['assets'][ball.image], (ball.rect.width, ball.rect.height), 'RGBA')
        paddle_image = pygame.image.fromstring(game_state.data['assets'][paddle.image], (paddle.rect.width, paddle.rect.height), 'RGBA')
        paddle2_image = pygame.image.fromstring(game_state.data['assets'][paddle2.image], (paddle.rect.width, paddle.rect.height), 'RGBA')

        # Draw the screen.
        self.screen.fill([0, 0, 0])
        self.screen.blit(ball_image, ball.rect)
        self.screen.blit(paddle_image, paddle.rect)
        self.screen.blit(paddle2_image, paddle2.rect)

        pygame.display.update()
        #print 'Drawing screen'