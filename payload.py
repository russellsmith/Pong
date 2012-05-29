game_state = 0 # Game state update.  Client sends its I/O, server updates game state and returns updated state.
asset_names = 1 # Client requests name of all assets.
asset_dict = 2 # Client requests assets as a dictionary, server sends all assets using pickle
asset_zip = 3 # Client requests assets as a zip, server zips and pickles all assets.


class Payload:
    def __init__(self, trans_type, data):
        self.transmission_type = trans_type
        self.data = data