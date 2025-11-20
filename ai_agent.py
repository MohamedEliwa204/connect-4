import math
import board
import copy


# agent is the player 2
class Heuristic():
    def __init__(self, ai_player, opp_player):
        self.ai_player = ai_player
        self.opp_player = opp_player

    def heuristic_evaluation(self, board):
        score_diff = 0
        score_diff += board.get_difference(2, 1) * 10000  # tha main in evaluation

        position_values = 0
        # horizontal
        for r in range(board.rows):
            for c in range(board.cols - 3):
                window = board.grid[r, c:c + 4]
                position_values += self.window_evaluations(window)

        # vertical
        for c in range(board.cols):
            for r in range(board.rows - 3):
                window = board.grid[r:r + 4, c]
                position_values += self.window_evaluations(window)

        # diagonal /
        for r in range(board.rows - 3):
            for c in range(board.cols - 3):
                window = [board.grid[r + i][c + i] for i in range(4)]
                position_values += self.window_evaluations(window)

        # diagonal \
        for r in range(3, board.rows):
            for c in range(board.cols - 3):
                window = [board.grid[r - i][c + i] for i in range(4)]
                position_values += self.window_evaluations(window)

        center_count = list(board.grid[:, 3]).count(self.ai_player)
        center_val = center_count * 4

        center_count = list(board.grid[:, 2]).count(self.ai_player) + list(board.grid[:, 4]).count(self.ai_player)
        center_val += center_count * 2
        return score_diff + position_values + center_val

    def window_evaluations(self, window):
        score = 0
        window = window.tolist()

        ai_pieces = window.count(self.ai_player)
        empty_slots = window.count(0)
        opp_pieces = window.count(self.opp_player)
        if ai_pieces == 3 and empty_slots == 1:
            score += 50
        elif ai_pieces == 2 and empty_slots == 2:
            score += 10

        if opp_pieces == 3 and empty_slots == 1:
            score -= 20
        elif opp_pieces == 2 and empty_slots == 2:
            score -= 8

        return score


class MiniMax():
    def __init__(self, board: board.Board, k_depth, heuristic: Heuristic, ai_player, opp_player):
        self.real_board = board  # I will clone it
        self.k_depth = k_depth
        self.heuristic = heuristic
        self.ai_player = ai_player
        self.opp_player = opp_player

    def get_best_move(self):
        simulation_board = self.real_board.copy()
        is_max = False
        best_eval = math.inf * -1
        best_col = -1
        for col in simulation_board.get_valid_cols():
            simulation_board.makemove(col, self.ai_player)
            eval = self.minimax(simulation_board, is_max, self.k_depth - 1)
            simulation_board.undomove()
            if eval > best_eval:
                best_eval = eval
                best_col = col

        return best_col

    def minimax(self, board: board.Board, is_max: bool, depth):
        if board.isterminal():
            #  check the winner
            diff = board.get_difference(self.ai_player, self.opp_player)

            return diff * 100000
        if depth == 0:
            return self.heuristic.heuristic_evaluation(board)

        if is_max:
            max_eval = math.inf * -1
            for col in board.get_valid_cols():
                board.makemove(col, self.ai_player)
                eval = self.minimax(board, False, depth - 1)
                board.undomove()
                max_eval = max(max_eval, eval)

            return max_eval
        if not is_max:
            min_eval = math.inf
            for col in board.get_valid_cols():
                board.makemove(col, self.opp_player)
                eval = self.minimax(board, True, depth - 1)
                board.undomove()
                min_eval = min(min_eval, eval)

            return min_eval


class MiniMaxAlphaBeta():
    def __init__(self, board: board.Board, k_depth, heuristic: Heuristic, ai_player, opp_player):
        self.real_board = board  # I will clone it
        self.k_depth = k_depth
        self.heuristic = heuristic
        self.ai_player = ai_player
        self.opp_player = opp_player

    def get_best_move(self):
        simulation_board = self.real_board.copy()
        is_max = False
        best_eval = math.inf * -1
        best_col = -1
        for col in simulation_board.get_valid_cols():
            simulation_board.makemove(col, self.ai_player)
            eval = self.minimax(simulation_board, is_max, math.inf * -1, math.inf, self.k_depth - 1)
            simulation_board.undomove()
            if eval > best_eval:
                best_eval = eval
                best_col = col

        return best_col

    def minimax(self, board: board.Board, is_max: bool, alpha, beta, depth):
        if board.isterminal():
            #  check the winner
            diff = board.get_difference(self.ai_player, self.opp_player)

            return diff * 100000
        if depth == 0:
            return self.heuristic.heuristic_evaluation(board)

        if is_max:
            max_eval = math.inf * -1
            for col in board.get_valid_cols():
                board.makemove(col, self.ai_player)
                eval = self.minimax(board, False, depth - 1)

                board.undomove()
                max_eval = max(max_eval, eval)
                alpha = max(max_eval, alpha)
                if beta <= alpha:
                    break

            return max_eval
        if not is_max:
            min_eval = math.inf
            for col in board.get_valid_cols():
                board.makemove(col, self.opp_player)
                eval = self.minimax(board, True, depth - 1)
                board.undomove()
                min_eval = min(min_eval, eval)
                beta = min(min_eval, beta)

                if beta <= alpha:
                    break

            return min_eval


class ExpectMinimax():
    pass