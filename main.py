import numpy as np

class Board():
    # 0 = Empty, 1 = Player 1, 2 = Player 2

    def __init__(self):
        self.rows = 6
        self.cols = 7

        self.grid = np.zeros((self.rows, self.cols), dtype=np.int8)  # to use smaller space
        self.col_heights = [0] * self.cols
        self.move_count = 0
        self.stack = []
        self.current_player = 1   # to keep track in undo

    def isvalidmove(self, col):
        return 0 <= col < self.cols and self.col_heights[col] < self.rows



    def makemove(self, col, player):

        if not self.isvalidmove(col):
            return False
        self.current_player = player
        row = self.col_heights[col]
        self.grid[row][col] = player
        self.col_heights[col] += 1
        self.move_count += 1
        self.stack.append(col)
        return True

    def undomove(self):
        col = self.stack.pop()
        row = self.col_heights[col] - 1
        if self.grid[row][col] == 1:
            self.current_player = 2
        elif self.grid[row][col] == 2:
            self.current_player = 1

        self.grid[row][col] = 0
        self.col_heights[col] -= 1
        self.move_count -= 1

    def isterminal(self):
        return self.move_count == self.rows * self.cols


    def coount_connected_four(self, player):
        count = 0
        piece_mask = (self.grid == player)

        #horizontal
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if np.all(piece_mask[r, c:c+4]):
                    count += 1



        #vertical
        for c in range(self.cols):
            for r in range(self.rows - 3):
                if np.all(piece_mask[r:r+4,c]):
                    count += 1


        #diagonal /
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if piece_mask[r, c] and piece_mask[r+1, c+1] and piece_mask[r+2, c+2] and piece_mask[r+3, c+3]:
                    count += 1

        #diagonal \
        for r in range(3,self.rows):
            for c in range(self.cols - 3):
                if piece_mask[r][c] and piece_mask[r-1][c+1] and piece_mask[r-2][c+2] and piece_mask[r-3][c+3]:
                    count += 1

        return count

    def get_valid_cols(self):
        return [col for col in range(self.cols) if self.col_heights[col] < self.rows]


