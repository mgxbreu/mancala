import time
import numpy as np


class MinimaxSolver():

    def __init__(self, max_depth=10, ts=None, max_time=None, timeit=False):
        self.max_depth = max_depth
        self.ts = ts
        self.max_time = max_time
        self.timeit = timeit

    def __maximize(self, state, alpha, beta, depth):

        if self.timeit:
            if time.time() - self.ts >= self.max_time:
                return (None, -np.inf)

        if state.is_game_over():
            return (None, state.evaluate())

        if depth >= self.max_depth:
            return (None, state.heuristic())

        max_child, max_utility = (None, -np.inf)

        for child in state.children():
            _, utility = self.__minimize(child, alpha, beta, depth + 1)
            if utility > max_utility:
                max_child, max_utility = child, utility

            if max_utility >= beta:
                break

            alpha = max(alpha, max_utility)

        return max_child, max_utility

    def __minimize(self, state, alpha, beta, depth):

        if self.timeit:
            if time.time() - self.ts >= self.max_time:
                return (None, -np.inf)

        if state.is_game_over():
            return (None, -state.evaluate())

        if depth >= self.max_depth:
            return (None, state.heuristic())

        min_child, min_utility = (None, np.inf)

        for child in state.children():

            _, utility = self.__maximize(child, alpha, beta, depth + 1)
            if utility < min_utility:
                min_child, min_utility = child, utility

            if min_utility <= alpha:
                break

            beta = min(beta, min_utility)

        return min_child, min_utility

    def solve(self, state):

        max_child, _ = self.__maximize(state, -np.inf, np.inf, 0)

        return max_child
