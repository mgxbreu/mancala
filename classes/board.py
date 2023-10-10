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
        self.game_finisher = None

    def get_next_turn(self):
        self.current_turn += 1
        if self.current_turn >= len(self.players):
            self.current_turn = 0
        return self.current_turn

    def change_board_perspective(self):
        first_half = self.board[:7]
        second_half = self.board[7:]

        self.board = second_half + first_half

    def change_turn(self):
        self.get_next_turn()
        self.change_board_perspective()

    def is_game_over(self):
        if all([len(pit.value) == 0 for pit in self.cluster_1]):
            self.game_finisher = self.players[0]
        elif all([len(pit.value) == 0 for pit in self.cluster_2]):
            self.game_finisher = self.players[1]

        store_1 = [
            pit for pit in self.board if pit.player.name == PLAYERS_NAMES[0] and pit.is_store()]
        store_2 = [
            pit for pit in self.board if pit.player.name == PLAYERS_NAMES[1] and pit.is_store()]

        print(self.cluster_1, 'cluster 1')
        print(self.cluster_2, 'cluster 2')
        print(store_1, 'store 1')
        print(store_2, 'store 2')

    def get_winner(self):
        self.is_game_over()
        if self.game_finisher:
            self.pick_and_sow_remaining_seeds()

        return self.game_finisher

    def pick_and_sow_remaining_seeds(self):
        print('pick_and_sow_remaining_seeds')
        remaining_seeds_cluster = [
            pit for pit in self.board if pit.player is not self.game_finisher
        ]

        store_to_sow = list(filter(lambda pit: pit.is_store(),
                              remaining_seeds_cluster))[0]

        remaining_seeds_cluster.remove(store_to_sow)
        print(store_to_sow)

        for pit in remaining_seeds_cluster:
            store_to_sow.value.extend(pit.value)
            pit.value = []
        print(store_to_sow)

    def make_a_move(self, move):
        move = int(move)
        # Number has to be 0-5
        seeds_on_pit = self.pick(move)
        if seeds_on_pit == 0:
            print('Invalid move')
            return None
        last_pit_sowed = self.sow(move, seeds_on_pit)
        if not self.is_extra_turn(last_pit_sowed):
            self.change_turn()
        else:
            print('Extra turn')
        return last_pit_sowed

    def pick(self, move):
        current_pit = self.board[move]
        seeds_on_pit = len(current_pit.value)
        current_pit.value = []
        return seeds_on_pit

    def sow(self, move, seeds_to_sow):
        pit_to_sow_in = None
        while seeds_to_sow > 0:
            move = (move + 1) % len(self.board)
            pit_to_sow_in = self.board[move]
            enemy_store = pit_to_sow_in.is_store(
            ) and pit_to_sow_in.player is not self.players[self.current_turn]
            if not enemy_store:
                pit_to_sow_in.value.append(Seed())
                seeds_to_sow -= 1
        return pit_to_sow_in

    def is_extra_turn(self, last_pit_sowed):
        return last_pit_sowed.is_store() and last_pit_sowed.player is self.players[self.current_turn]

    def start_game(self):
        self.initialize_players()
        self.initialize_seeds()
        self.cluster_1 = [
            pit for pit in self.board if pit.player.name == PLAYERS_NAMES[0] and not pit.is_store()]
        self.cluster_2 = [
            pit for pit in self.board if pit.player.name == PLAYERS_NAMES[1] and not pit.is_store()]

    def initialize_players(self):
        for name in PLAYERS_NAMES:
            player = Player(name)
            for _ in range(6):
                pit = Pit(player)
                self.board.append(pit)

            store = Store(player)
            self.board.append(store)
            self.players.append(player)

    def initialize_seeds(self):
        for pit in self.board:
            if not pit.is_store():
                pit.value = [Seed() for _ in range(1)]

    def __str__(self):
        board_string = f'{self.board}\n'
        # board_string += f'\t{self.board[0].pits}\n'
        # board_string += f'\t\t\t\t\t\t\t\t\t\t\t\t{self.board[1].store}\n'
        # board_string += f'\t{self.board[1].pits}'
        # board_string = f'{self.board[0].store} {self.board[0].pits[::-1]}\n'
        # board_string += f'{self.board[1]}'

        return board_string
