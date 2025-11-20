import math

# agent is the player 2
class heuristic():
    def __init__(self, ai_player, opp_player):
        self.ai_player = ai_player
        self.opp_player = opp_player



    def heuristic_evaluation(self, board):
        score_diff = 0
        score_diff += board.get_difference(2, 1) * 10000  # tha main in evaluation

        position_values = 0
        #horizontal
        for r in range(board.rows):
            for c in range(board.cols - 3):
                window = board.grid[r, c:c+4]
                position_values += self.window_evaluations(window)


        #vertical
        for c in range(board.cols):
            for r in range(board.rows - 3):
                window = board.grid[r:r+4, c]
                position_values += self.window_evaluations(window)


        #diagonal /
        for r in range(board.rows - 3):
            for c in range(board.cols - 3):
                window = [board.grid[r+i][c+i] for i in range(4)]
                position_values += self.window_evaluations(window)


        #diagonal \
        for r in range(3,board.rows):
            for c in range(board.cols - 3):
                window = [board.grid[r-i][c+i] for i in range(4)]
                position_values += self.window_evaluations(window)


        center_count = list(board.grid[:, 3]).count(self.ai_player)
        center_val = center_count * 4

        center_count = list(board.grid[:, 2]).count(self.ai_player) + list(board.grid[:,4]).count(self.ai_player)
        center_val += center_count * 2
        return  score_diff + position_values + center_val

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
    def __init__(self, board, k_depth):
        self.board = board
        self.k_depth = k_depth

    def get_best_move(self):
        pass

    def minimax(self, is_max, depth):
        pass






