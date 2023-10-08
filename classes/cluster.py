from classes.store import Store
from classes.pit import Pit


class Cluster:
    def __init__(self, player):
        self.pits = [Pit() for _ in range(6)]
        self.store = Store()
        self.player = player
        self.values = [self.store, *self.pits]

    def __str__(self):
        return f'{self.values}'

    def __repr__(self):
        return f'{self.values}'
