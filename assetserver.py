from baseserver import *
import payload

class AssetServer(BaseServer):

    def receive(self, p, connection):
        if p.transmission_type == game_state:
            user_input = p.data['user_input']
            self.game_tick(user_input)

            # Prepare and send updated game state to user
            data = { 'actors' : self.actors,
            }
            p = Payload(game_state, data)
            packet = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
            #self.send(packet, connection)
            connection.send(packet)
        elif p.transmission_type == asset_dict:
            assets_needed = p.data['assets_needed']
            asset_values = {}
            for a in assets_needed:
                asset_values[a] = self.assets[a]
            data = {'assets_needed' : asset_values }
            p = Payload(asset_dict, data)
            packet = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
            connection.send(packet)