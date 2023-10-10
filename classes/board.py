from consts import PLAYERS_NAMES
from classes.player import Player
# from classes.cluster import Cluster
from classes.pit import Pit
from classes.store import Store
from classes.seed import Seed


class Board:
    def __init__(self):
        self.board = []
        self.winner = None
        self.players = []
        self.current_turn = 0

    def get_current_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)
        return self.current_turn

    def make_a_move(self, move):
        move = int(move)
        # Number has to be 0-5
        seeds_on_pit = self.pick(move)
        self.sow(move, seeds_on_pit)

    def pick(self, move):
        current_pit = self.board[move]
        seeds_on_pit = len(current_pit.value)
        current_pit.value = []
        return seeds_on_pit

    def sow(self, move, seeds_to_sow):
        while seeds_to_sow > 0:
            move = (move + 1) % len(self.board)
            pit_to_sow_in = self.board[move]
            pit_to_sow_in.value.append(Seed())
            seeds_to_sow -= 1

    def start_game(self):
        self.initialize_players()
        self.initialize_seeds()

    def initialize_players(self):
        for name in PLAYERS_NAMES:
            player = Player(name)
            for _ in range(6):
                pit = Pit(player)
                self.board.append(pit)

            store = Store(player)
            self.board.append(store)

    def initialize_seeds(self):
        for pit in self.board:
            if not pit.is_store():
                pit.value = [Seed() for _ in range(4)]

    def __str__(self):
        board_string = f'{self.board}\n'
        # board_string += f'\t{self.board[0].pits}\n'
        # board_string += f'\t\t\t\t\t\t\t\t\t\t\t\t{self.board[1].store}\n'
        # board_string += f'\t{self.board[1].pits}'
        # board_string = f'{self.board[0].store} {self.board[0].pits[::-1]}\n'
        # board_string += f'{self.board[1]}'

        return board_string
