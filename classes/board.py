from consts import PLAYERS_NAMES
from classes.player import Player
from classes.cluster import Cluster
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
        seeds_on_pit = self.pick(move)
        self.sow(move, seeds_on_pit)

    def pick(self, move):
        current_pit = self.board[self.current_turn].pits
        seeds_on_pit = len(current_pit[move].value)
        current_pit[move].value = []
        return seeds_on_pit

    # def sow(self, move, seeds_on_pit):
    #     for _ in range(seeds_on_pit):
        # move = (move + 1) % len(self.board[self.current_turn].pits)
        # self.board[self.current_turn].pits[move].value.append(Seed())

    def start_game(self):
        self.initialize_players()
        self.initialize_seeds()

    def initialize_players(self):
        for name in PLAYERS_NAMES:
            player = Player(name)
            cluster = Cluster(player)
            self.board.append(cluster)
            self.players.append(player)

    def initialize_seeds(self):
        for cluster in self.board:
            for pit in cluster.pits:
                pit.value = [Seed() for _ in range(4)]

    def __str__(self):
        board_string = f'{self.board[0].store}\n'
        board_string += f'\t{self.board[0].pits}\n'
        board_string += f'\t\t\t\t\t\t\t\t\t\t\t\t{self.board[1].store}\n'
        board_string += f'\t{self.board[1].pits[::-1]}'

        return board_string
