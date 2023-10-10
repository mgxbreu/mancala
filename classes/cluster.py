from classes.store import Store
from classes.pit import Pit


class Cluster:
    def __init__(self, values=0):
        self.pits = [Pit() for _ in range(6)]
        self.store = Store()
        self.values = [self.store, *self.pits] if values == 0 else [*self.pits, self.store]

    def __str__(self):
        return f'{self.values}'

    def __repr__(self):
        return f'{self.values}'
