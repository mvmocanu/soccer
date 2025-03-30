class BaseClient:
    def __init__(self, num_players=5):
        self.num_players = num_players

    def fetch_players(self):
        raise NotImplementedError
