from baseserver import *
import payload

class ObjectServer(BaseServer):
    """A type of server that serializes and sends all art assets and actors each game update.

    Actors data is expected by the client to be in a dictionary with key name 'actors'.

    Assets data is expected by the client to be in a dictionary with key name 'assets'.

    """

    def receive(self, p, connection):
        """Listens only for a game state transmission type.

        User input states are in a dictionary passed in the Payload object p.  The key is user_input,
        so to access user_input values you can get them with the following assignment:
        user_input = p.data['user_input']

        Update the game state and create a dictionary with keys 'actors' and 'assets' storing the
        actors and assets dictionaries respectively.  Store these in a Payload packet of type game_state,
        pickle the object and send it using the connection object.

        For more information on the Python pickle module see:
        1) http://docs.python.org/library/pickle.html
        2) http://wiki.python.org/moin/UsingPickle


        """
        if p.transmission_type == game_state:
            """Grab the user input states from the payload packet.  Use this value to perform a game_tick (the game_tick function
            can be found in BaseServer.py and can be called by referencing it as self.game_tick(parameter) where parameter
            represents the correct parameters.
            """
            user_input = p.data['user_input']
            self.game_tick(user_input)

            """Prepare and send updated game state to user
            """
            data = { 'actors' : self.actors,
                     'assets' : self.assets
            }
            p = Payload(game_state, data)
            packet = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
            connection.send(packet)