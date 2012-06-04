game_state = 0 # Game state update.  Client sends its I/O, server updates game state and returns updated state.
asset_dict = 1 # Client requests assets as a dictionary, server sends all assets using pickle
asset_zip = 2 # Client requests assets as a zip, server zips and pickles all assets.


class Payload:
    """A container for information sent to and from the server.

    Data:
    transmission_type -- A flag identifying what the information stored in the object represents.
    data -- The data itself.
    """
    def __init__(self, trans_type, data):
        self.transmission_type = trans_type
        self.data = data