from baseserver import *
import zipfile
import StringIO
import payload

class ZipServer(BaseServer):
    """A type of server that receives game state and asset requests as separate queries.  Asset requests are of
    transmission type asset_zip defined in Payload.py.  Asset queries are zipped prior to sending them over the socket.

    Actors data is expected by the client to be in a dictionary with key name 'actors' in game_state updates.

    Assets data is expected by the client to be in a dictionary with key name 'assets_needed' in asset_zip requests.

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
            connection.send(packet)
        elif p.transmission_type == asset_zip:
            """
            The client is requesting a zip of assets.  Send a zip back containing all requested art assets.  Examine
            the Python ZipFile module for creating zips of assets:
            http://docs.python.org/library/zipfile.html

            A list containing names of all requested assets can be found in p.data['assets_needed']

            """
            in_memory_zip = StringIO.StringIO()
            zf = zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED, False)
            assets_needed = p.data['assets_needed']
            asset_values = {}
            for a in assets_needed:
                zf.writestr(a, self.assets[a])
            data = {'assets_needed' : zf }
            p = Payload(asset_dict, data)
            packet = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
            connection.send(packet)