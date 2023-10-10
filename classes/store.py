from classes.pit import Pit


class Store(Pit):
    def __init__(self, player):
        super().__init__(player)

    def is_store(self):
        return True
