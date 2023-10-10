
from classes.board import Board


def main():

    board = Board()
    board.start_game()
    winner = board.check_for_winner()

    while winner is None:
        print(board)
        pit_to_sow = input('Enter your move' + '\n')
        board.make_a_move(pit_to_sow)
        print(board)
        winner = board.check_for_winner()
        print(f"The winner is {winner}")


main()
