from consts import PLAYERS_NAMES
from classes.player import Player
from classes.pit import Pit
from classes.store import Store
from classes.seed import Seed
from copy import deepcopy
import numpy as np



class Board:
    def __init__(self, board=None, turn=None):
        self.board = board if board is not None else []
        self.winner = None
        self.players = []
        self.current_turn = turn if turn is not None else 0
        self.game_finisher = None
        self.last_player_to_play = None

    def get_next_turn(self):
        self.current_turn += 1
        if self.current_turn >= len(self.players):
            self.current_turn = 0
        return self.current_turn

    def change_board_perspective(self):
        first_half = self.board[:7]
        second_half = self.board[7:]

        return second_half + first_half

    def change_turn(self):
        self.get_next_turn()
        self.board = self.change_board_perspective()

    def is_game_over(self):
        if all([len(pit.value) == 0 for pit in self.cluster_1]):
            self.game_finisher = self.players[0]
            return True
        elif all([len(pit.value) == 0 for pit in self.cluster_2]):
            self.game_finisher = self.players[1]
            return True
        return False

    def get_winner(self):
        self.is_game_over()
        if self.game_finisher:
            self.pick_and_sow_remaining_seeds()
            self.count_seeds()
            self.decide_winner()

        return self.winner

    def pick_and_sow_remaining_seeds(self):
        remaining_seeds_cluster = [
            pit for pit in self.board if pit.player is not self.game_finisher
        ]

        store_to_sow = list(filter(lambda pit: pit.is_store(),
                                   remaining_seeds_cluster))[0]

        remaining_seeds_cluster.remove(store_to_sow)

        for pit in remaining_seeds_cluster:
            store_to_sow.value.extend(pit.value)
            pit.value = []

    def count_seeds(self):
        self.players[0].score = len(self.store_1.value)
        self.players[1].score = len(self.store_2.value)

    def decide_winner(self):
        self.winner = self.players[1]
        if self.players[0].score > self.players[1].score:
            self.winner = self.players[0]

    def was_my_last_pit_empty(self, last_pit_sowed):
        return len(last_pit_sowed.value) == 1 and not last_pit_sowed.is_store()

    def capture_seeds(self, last_pit_sowed, move):
        if last_pit_sowed.player == self.players[0]:
            move += 1
        last_pit_sowed_index = self.board.index(last_pit_sowed)
        self.pick(last_pit_sowed_index)

        inverted_board = self.change_board_perspective()
        opposite_last_pit = inverted_board[move]

        opposite_last_pit_index = self.board.index(opposite_last_pit)

        # seed from last_pit_sowed
        seeds_on_pit = self.pick(opposite_last_pit_index) + 1

        if seeds_on_pit == 0:
            return
        current_store = list(filter(lambda pit: pit.is_store() and pit.player == self.players[self.current_turn],
                                    self.board))[0]
        current_store.value.extend(list(Seed() for _ in range(seeds_on_pit)))

    def make_a_move(self, move):
        extra_turn = False
        move = int(move)
        if move > 5 or move < 0:
            print('Invalid move. Number has to be 0-5')
            return (None, extra_turn)
        seeds_on_pit = self.pick(move)
        if seeds_on_pit == 0:
            print('Invalid move. Pit must have seeds')
            return (None, extra_turn)
        last_pit_sowed = self.sow(move, seeds_on_pit)

        # if self.was_my_last_pit_empty(last_pit_sowed):
        #     self.capture_seeds(last_pit_sowed, move)

        self.last_player_to_play = self.players[self.current_turn]
        if not self.is_extra_turn(last_pit_sowed):
            self.change_turn()
        else:
            print('Extra turn')
            extra_turn = True
            
        return last_pit_sowed, extra_turn

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
        self.store_1 = [
            pit for pit in self.board if pit.player.name == PLAYERS_NAMES[0] and pit.is_store()][0]
        self.store_2 = [
            pit for pit in self.board if pit.player.name == PLAYERS_NAMES[1] and pit.is_store()][0]

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
                pit.value = [Seed() for _ in range(4)]

    def children(self):
        children = []
        for move in range(6):
            child = deepcopy(self)
            last_pit_sowed, extra_turn = child.make_a_move(move)
            if last_pit_sowed:
                children.append((child, extra_turn))
        return children
    
    def get_cluster_points(self, turn):
        if turn == 0:
            cluster_seeds = sum([len(x.value) for x in self.cluster_1 ]) 
            store_seeds = len(self.store_1.value)
            return cluster_seeds + store_seeds
        else:
            cluster_seeds = sum([len(x.value) for x in self.cluster_2 ]) 
            store_seeds = len(self.store_2.value)
            return cluster_seeds + store_seeds

    
    def heuristic(self):
        return  len(self.store_2.value) - len(self.store_1.value)
    
    def evaluate(self):
        self.get_winner()
        if self.winner:
            if self.winner == self.last_player_to_play:
                return 1 * np.inf
            else:
                return -1 * np.inf

    def __str__(self):
        board_string = ""
        board_string += f'\t|{self.board[7:13][::-1]}|\n'
        board_string += f'{self.board[13]} \t|------------------|\t {self.board[6]}\n'
        board_string += f'\t|{self.board[:6]}|\n'
        return board_string
