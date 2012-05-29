from baseserver import *
import zipfile
import StringIO
import payload

class ZipServer(BaseServer):

    def receive(self, p, connection):
        if p.transmission_type == game_state:
            user_input = p.data['user_input']
            self.game_tick(user_input)

            # Prepare and send updated game state to user
            data = { 'actors' : self.actors,
            }
            p = Payload(game_state, data)
            packet = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
            connection.send(packet)
        elif p.transmission_type == asset_zip:
            in_memory_zip = StringIO.StringIO()
            zf = zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED, False)
            assets_needed = p.data['assets_needed']
            asset_values = {}
            for a in assets_needed:
                zf.writestr(a, self.assets[a])
            #zf.close()
            data = {'assets_needed' : zf }
            p = Payload(asset_dict, data)
            packet = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
            connection.send(packet)