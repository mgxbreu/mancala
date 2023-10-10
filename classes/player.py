class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def __str__(self):
        return f'{self.name}'
