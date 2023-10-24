
from classes.board import Board
from classes.minimax_algorithm import MinimaxSolver
import time
import os

def main():

    board = Board()
    board.start_game()
    winner = board.get_winner()

    print(board) 
    while winner is None:
        if board.current_turn == 0:
            pit_to_sow = input('Enter your move' + '\n')
            board.make_a_move(pit_to_sow)

        else:
            max_time = 0.5
            minimax_solver = MinimaxSolver(max_time=max_time, ts=time.time())

            best_state = None
            ts = time.time()
            for depth in range(1,3):
                minimax_solver.max_depth = depth
                best_state = minimax_solver.solve(board)
                if time.time() - ts >= max_time:
                    break

            board = best_state if best_state is not None else board 
        os.system('cls')
        print(board)
        winner = board.get_winner()
    print(f"{board.players[0]} total point(s): {board.players[0].score}")
    print(f"{board.players[1]} total point(s): {board.players[1].score}")
    print(f"The winner is {winner}")


main()
