from baseclient import *
import payload
import pickle

class AssetClient(BaseClient):
    """A type of client that expects the server to send the current game state each frame.  Assets are not sent
    unless requested with an asset_dict Payload request sent to the server.

    Actors data is expected to be in a dictionary with key name 'actors'.  This dictionary should have Actor objects
    'ball', 'player1', and 'player2' representing the ball, the player and the computer player respectively.

    Asset request response data is expected to be in a dictionary with key name 'assets_needed'.

    """
    def request_assets(self, game_state):
        """Scans the Actors sent through a game state update and requests any assets that aren't currently stored
        locally.
        """
        assets_needed = []
        actors = game_state.data['actors']

        # Finds any asset names that aren't currently stored locally
        for actor_name, actor in actors.iteritems():
            if not actor.image in self.assets:
                assets_needed.append(actor.image)

        # If our asset list has at least one value we need to request them from the server
        if assets_needed:
            data = {'assets_needed' : assets_needed}
            p = Payload(asset_dict, data)
            self.send(p)
            received = None
            while not received:
                received = self.socket.recv(self.buffer_size)
                if received:
                    asset_data = pickle.loads(received)
                    for asset in asset_data.data['assets_needed'].iterkeys():
                        self.assets[asset] = asset_data.data['assets_needed'][asset]

    def receive(self):
        received = self.socket.recv(self.buffer_size)

        if received:
            game_state = pickle.loads(received)
            self.request_assets(game_state)
            return game_state
        else:
            return None

    def draw_screen(self, game_state):
        ball = game_state.data['actors']['ball']
        paddle = game_state.data['actors']['player1']
        paddle2 = game_state.data['actors']['player2']

        ball_image = pygame.image.fromstring(self.assets[ball.image], (ball.rect.width, ball.rect.height), 'RGBA')
        paddle_image = pygame.image.fromstring(self.assets[paddle.image], (paddle.rect.width, paddle.rect.height), 'RGBA')
        paddle2_image = pygame.image.fromstring(self.assets[paddle2.image], (paddle.rect.width, paddle.rect.height), 'RGBA')

        self.screen.fill([0, 0, 0])
        self.screen.blit(ball_image, ball.rect)
        self.screen.blit(paddle_image, paddle.rect)
        self.screen.blit(paddle2_image, paddle2.rect)

        pygame.display.update()
        print 'Drawing screen'

