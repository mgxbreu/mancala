class Pit:
    def __init__(self, player):
        self.player = player
        self.value = []

    def __str__(self):
        return f'{len(self.value)}'

    def __repr__(self):
        return f'{len(self.value)}'

    def is_store(self):
        return False
