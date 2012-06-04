from baseclient import *
import payload
import zipfile
import StringIO
import pickle

class ZipClient(BaseClient):
    def request_assets(self, game_state):
        assets_needed = []
        actors = game_state.data['actors']

        for actor_name, actor in actors.iteritems():
            if not actor.image in self.assets:
                assets_needed.append(actor.image)

        if assets_needed:
            data = {'assets_needed' : assets_needed}
            p = Payload(asset_zip, data)
            self.send(p)
            received = None
            while not received:
                received = self.socket.recv(self.buffer_size)
                if received:
                    asset_data = pickle.loads(received)
                    zf = asset_data.data['assets_needed']
                    for f in zf.namelist():
                        file = zf.read(f)
                        self.assets[f] = file
                    zf.close()


    def receive(self):
        received = self.socket.recv(self.buffer_size)

        if received:
            # Unpickle the payload
            game_state = pickle.loads(received)

            # Check and request any assets needed
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
        #print 'Drawing screen'

