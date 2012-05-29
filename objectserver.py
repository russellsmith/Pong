from baseserver import *
import payload

class ObjectServer(BaseServer):

    def receive(self, p, connection):
        if p.transmission_type == game_state:
            user_input = p.data['user_input']
            self.game_tick(user_input)

            # Prepare and send updated game state to user
            data = { 'actors' : self.actors,
                     'assets' : self.assets
            }
            p = Payload(game_state, data)
            packet = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
            #self.send(packet, connection)
            connection.send(packet)