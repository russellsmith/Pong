from baseserver import *
import payload

class AssetServer(BaseServer):
    """A type of server that receives game state and asset requests as separate queries.  Asset requests are of
    transmission type asset_dict defined in Payload.py.

    Actors data is expected by the client to be in a dictionary with key name 'actors' in game_state updates.

    Assets data is expected by the client to be in a dictionary with key name 'assets_needed' in asset_dict requests.

    """

    def receive(self, p, connection):
        if p.transmission_type == game_state:
            """
            The client is requesting a game state.
            """
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
            """
            The client is requesting a dictionary of assets.  Send a dictionary back containing key-value pairs
            where the key is the name of an asset requested and the value is the image itself.

            A list containing names of all requested assets can be found in p.data['assets_needed']

            """
            assets_needed = p.data['assets_needed']
            asset_values = {}
            for a in assets_needed:
                asset_values[a] = self.assets[a]
            data = {'assets_needed' : asset_values }
            p = Payload(asset_dict, data)
            packet = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
            connection.send(packet)