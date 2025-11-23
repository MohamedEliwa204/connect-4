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
                eval = self.minimax(board, False,alpha, beta, depth - 1)

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
                eval = self.minimax(board, False, alpha, beta, depth - 1)
                board.undomove()
                min_eval = min(min_eval, eval)
                beta = min(min_eval, beta)

                if beta <= alpha:
                    break

            return min_eval


class ExpectMinimax():
    def __init__(self, board_obj, k_depth, heuristic, ai_player, opp_player):
        self.real_board = board_obj
        self.k_depth = k_depth
        self.heuristic = heuristic
        self.ai_player = ai_player
        self.opp_player = opp_player

    def get_best_move(self):
        simulation_board = self.real_board.copy()
        best_eval = -math.inf
        best_col = -1
        valid_cols = simulation_board.get_valid_cols()

        if len(valid_cols) == 1:
            return valid_cols[0]

        for col in valid_cols:
            eval = self.calculate_chance_node(simulation_board, col, self.k_depth - 1, False)
            
            print(f"Col {col}: Expected Score {eval:.2f}")

            if eval > best_eval:
                best_eval = eval
                best_col = col
        
        return best_col if best_col != -1 else valid_cols[0]

    def expectiminimax(self, board_obj, depth, is_max):
        if depth == 0 or board_obj.isterminal():
            if board_obj.isterminal():
                return board_obj.get_difference(self.ai_player, self.opp_player) * 100000
            return self.heuristic.heuristic_evaluation(board_obj)

        if is_max:
            max_eval = -math.inf
            for col in board_obj.get_valid_cols():
                current_val = self.calculate_chance_node(board_obj, col, depth - 1, False)
                max_eval = max(max_eval, current_val)
            return max_eval
        else:
            min_eval = math.inf
            for col in board_obj.get_valid_cols():
                current_val = self.calculate_chance_node(board_obj, col, depth - 1, True)
                min_eval = min(min_eval, current_val)
            return min_eval

    def calculate_chance_node(self, board_obj, intended_col, next_depth, next_is_max):
        prob_intended = 0.6
        prob_left = 0.2
        prob_right = 0.2
        
        col_left = intended_col - 1
        col_right = intended_col + 1
        
        if col_left < 0:
            prob_intended += prob_left
            prob_left = 0
            
        if col_right >= board_obj.cols:
            prob_intended += prob_right
            prob_right = 0

        expected_value = 0
        current_player = self.ai_player if not next_is_max else self.opp_player
        
        possible_moves = [
            (intended_col, prob_intended),
            (col_left, prob_left),
            (col_right, prob_right)
        ]

        total_prob = 0

        for col, prob in possible_moves:
            if prob > 0:
                if board_obj.isvalidmove(col):
                    board_obj.makemove(col, current_player)
                    val = self.expectiminimax(board_obj, next_depth, next_is_max)
                    board_obj.undomove()
                    
                    expected_value += val * prob
                    total_prob += prob
                else:
                    pass
        
        if total_prob > 0:
            return expected_value / total_prob
        else:
            return -math.inf if not next_is_max else math.inf