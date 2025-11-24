import math
import board
import copy
import time


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m' # For Max
    RED = '\033[91m'   # For Min
    YELLOW = '\033[93m' # For Pruning
    RESET = '\033[0m'

class Heuristic():
    def __init__(self, ai_player, opp_player):
        self.ai_player = ai_player
        self.opp_player = opp_player

    def heuristic_evaluation(self, board):
        score_diff = 0
        score_diff += board.get_difference(self.ai_player, self.opp_player) * 10000

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
        if hasattr(window, 'tolist'):
            window = window.tolist()
        else:
            window = list(window)
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
    def __init__(self, board_obj, k_depth, heuristic, ai_player, opp_player):
        self.real_board = board_obj
        self.k_depth = k_depth
        self.heuristic = heuristic
        self.ai_player = ai_player
        self.opp_player = opp_player
        self.node_expanded = 0
        self.execution_time = 0

    def get_best_move(self, visualize=True):
        self.node_expanded=0
        start_time = time.time()
        simulation_board = self.real_board.copy()
        best_eval = math.inf * -1
        best_col = -1

        print(f"{Colors.HEADER}--- STARTING MINIMAX (Depth {self.k_depth}) ---{Colors.RESET}")

        for col in simulation_board.get_valid_cols():
            simulation_board.makemove(col, self.ai_player)


            if visualize: print(f"{Colors.GREEN}Root checking Col {col}...{Colors.RESET}")

            eval = self.minimax(simulation_board, False, self.k_depth - 1, visualize)
            simulation_board.undomove()

            if visualize: print(f"{Colors.GREEN}Root Col {col} -> Eval: {eval}{Colors.RESET}")

            if eval > best_eval:
                best_eval = eval
                best_col = col
        self.execution_time = time.time()-start_time
        print(f"{Colors.HEADER}--- BEST MOVE: {best_col} (Eval: {best_eval}) ---{Colors.RESET}")
        return best_col

    def minimax(self, board_obj, is_max, depth, visualize):
        self.node_expanded+=1

        indent = "|   " * (self.k_depth - depth)
        node_type = f"{Colors.GREEN}MAX{Colors.RESET}" if is_max else f"{Colors.RED}MIN{Colors.RESET}"

        if board_obj.isterminal():
            diff = board_obj.get_difference(self.ai_player, self.opp_player)
            val = diff * 100000
            if visualize: print(f"{indent}L {node_type} Terminal: {val}")
            return val

        if depth == 0:
            val = self.heuristic.heuristic_evaluation(board_obj)

            return val

        if is_max:
            max_eval = math.inf * -1
            for col in board_obj.get_valid_cols():
                board_obj.makemove(col, self.ai_player)
                eval = self.minimax(board_obj, False, depth - 1, visualize)
                board_obj.undomove()

                if visualize: print(f"{indent}|-- {node_type} (Col {col}): {eval}")
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for col in board_obj.get_valid_cols():
                board_obj.makemove(col, self.opp_player)
                eval = self.minimax(board_obj, True, depth - 1, visualize)
                board_obj.undomove()

                if visualize: print(f"{indent}|-- {node_type} (Col {col}): {eval}")
                min_eval = min(min_eval, eval)
            return min_eval


class MiniMaxAlphaBeta():
    def __init__(self, board_obj, k_depth, heuristic, ai_player, opp_player):
        self.real_board = board_obj
        self.k_depth = k_depth
        self.heuristic = heuristic
        self.ai_player = ai_player
        self.opp_player = opp_player
        self.node_expanded = 0
        self.execution_time = 0

    def get_best_move(self, visualize=True):
        self.node_expanded=0
        start_time = time.time()
        simulation_board = self.real_board.copy()
        best_eval = math.inf * -1
        best_col = -1

        print(f"{Colors.HEADER}--- STARTING ALPHA-BETA (Depth {self.k_depth}) ---{Colors.RESET}")

        for col in simulation_board.get_valid_cols():
            simulation_board.makemove(col, self.ai_player)
            if visualize: print(f"{Colors.GREEN}Root checking Col {col}...{Colors.RESET}")

            eval = self.minimax(simulation_board, False, math.inf * -1, math.inf, self.k_depth - 1, visualize)
            simulation_board.undomove()

            if visualize: print(f"{Colors.GREEN}Root Col {col} -> Eval: {eval}{Colors.RESET}")

            if eval > best_eval:
                best_eval = eval
                best_col = col
        self.execution_time = time.time()-start_time
        print(f"{Colors.HEADER}--- BEST MOVE: {best_col} (Eval: {best_eval}) ---{Colors.RESET}")
        return best_col

    def minimax(self, board_obj, is_max, alpha, beta, depth, visualize):
        self.node_expanded+=1
        indent = "|   " * (self.k_depth - depth)
        node_type = f"{Colors.GREEN}MAX{Colors.RESET}" if is_max else f"{Colors.RED}MIN{Colors.RESET}"

        if board_obj.isterminal():
            diff = board_obj.get_difference(self.ai_player, self.opp_player)
            return diff * 100000
        if depth == 0:
            return self.heuristic.heuristic_evaluation(board_obj)

        if is_max:
            max_eval = math.inf * -1
            for col in board_obj.get_valid_cols():
                board_obj.makemove(col, self.ai_player)
                eval = self.minimax(board_obj, False, alpha, beta, depth - 1, visualize)
                board_obj.undomove()

                max_eval = max(max_eval, eval)
                alpha = max(max_eval, alpha)

                if visualize:
                    print(f"{indent}|-- {node_type} Col {col}: {eval} [α:{alpha}, β:{beta}]")

                if beta <= alpha:
                    if visualize: print(f"{indent}{Colors.YELLOW}*** PRUNED (Beta {beta} <= Alpha {alpha}) ***{Colors.RESET}")
                    break

            return max_eval
        else:
            min_eval = math.inf
            for col in board_obj.get_valid_cols():
                board_obj.makemove(col, self.opp_player)

                eval = self.minimax(board_obj, True, alpha, beta, depth - 1, visualize)
                board_obj.undomove()

                min_eval = min(min_eval, eval)
                beta = min(min_eval, beta)

                if visualize:
                    print(f"{indent}|-- {node_type} Col {col}: {eval} [α:{alpha}, β:{beta}]")

                if beta <= alpha:
                    if visualize: print(f"{indent}{Colors.YELLOW}*** PRUNED (Beta {beta} <= Alpha {alpha}) ***{Colors.RESET}")
                    break

            return min_eval


class ExpectMinimax():
    def __init__(self, board_obj, k_depth, heuristic, ai_player, opp_player):
        self.real_board = board_obj
        self.k_depth = k_depth
        self.heuristic = heuristic
        self.ai_player = ai_player
        self.opp_player = opp_player
        self.node_expanded = 0
        self.execution_time = 0

    def get_best_move(self, visualize=True):
        self.node_expanded=0
        start_time = time.time()
        simulation_board = self.real_board.copy()
        best_eval = -math.inf
        best_col = -1
        valid_cols = simulation_board.get_valid_cols()

        print(f"{Colors.HEADER}--- STARTING EXPECTIMINIMAX ---{Colors.RESET}")

        if len(valid_cols) == 1:
            return valid_cols[0]

        for col in valid_cols:
            if visualize: print(f"{Colors.GREEN}Root checking Col {col}...{Colors.RESET}")
            eval = self.calculate_chance_node(simulation_board, col, self.k_depth - 1, False, visualize)

            if visualize: print(f"{Colors.GREEN}Expected Score Col {col}: {eval:.2f}{Colors.RESET}")

            if eval > best_eval:
                best_eval = eval
                best_col = col
        self.execution_time = time.time()-start_time
        return best_col if best_col != -1 else valid_cols[0]

    def expectiminimax(self, board_obj, depth, is_max, visualize):
        self.node_expanded += 1
        indent = "|   " * (self.k_depth - depth)
        if depth == 0 or board_obj.isterminal():
            if board_obj.isterminal():
                return board_obj.get_difference(self.ai_player, self.opp_player) * 100000
            return self.heuristic.heuristic_evaluation(board_obj)

        if is_max:
            max_eval = -math.inf
            for col in board_obj.get_valid_cols():
                current_val = self.calculate_chance_node(board_obj, col, depth - 1, False, visualize)
                if visualize: print(f"{indent}|-- MAX Node Col {col} -> Chance Val: {current_val:.1f}")
                max_eval = max(max_eval, current_val)
            return max_eval
        else:
            min_eval = math.inf
            for col in board_obj.get_valid_cols():
                current_val = self.calculate_chance_node(board_obj, col, depth - 1, True, visualize)
                if visualize: print(f"{indent}|-- MIN Node Col {col} -> Chance Val: {current_val:.1f}")
                min_eval = min(min_eval, current_val)
            return min_eval

    def calculate_chance_node(self, board_obj, intended_col, next_depth, next_is_max, visualize):

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

        indent = "|   " * (self.k_depth - next_depth) + "   "

        for col, prob in possible_moves:
            if prob > 0 and board_obj.isvalidmove(col):
                board_obj.makemove(col, current_player)
                val = self.expectiminimax(board_obj, next_depth, next_is_max, visualize)
                board_obj.undomove()


                if visualize and next_depth > 0:
                    print(f"{indent}~ Chance: Intended {intended_col} -> Fell {col} ({int(prob*100)}%) = Val {val:.1f}")

                expected_value += val * prob
                total_prob += prob

        if total_prob > 0:
            return expected_value / total_prob
        else:
            return -math.inf if not next_is_max else math.inf