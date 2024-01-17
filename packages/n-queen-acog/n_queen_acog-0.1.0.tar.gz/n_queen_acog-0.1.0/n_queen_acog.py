"""
N-Queens Solver Library

This module provides a class, NQueensSolver, for solving the N-Queens problem using backtracking.
"""

class NQueensSolver:
    def __init__(self):
        pass

    def isSafe(self, row, col, board, n):
        duprow, dupcol = row, col

        while row >= 0 and col >= 0:
            if board[row][col] == 'Q':
                return False
            row -= 1
            col -= 1

        col, row = dupcol, duprow
        while col >= 0:
            if board[row][col] == 'Q':
                return False
            col -= 1

        row, col = duprow, dupcol
        while row < n and col >= 0:
            if board[row][col] == 'Q':
                return False
            row += 1
            col -= 1

        return True

    def solve(self, col, board, ans, n):
        if col == n:
            ans.append([row[:] for row in board])
            return

        for row in range(n):
            if self.isSafe(row, col, board, n):
                board[row][col] = 'Q'
                self.solve(col + 1, board, ans, n)
                board[row][col] = '.'

    def solveNQueens(self, n):
        ans = []
        board = [['.' for _ in range(n)] for _ in range(n)]
        self.solve(0, board, ans, n)
        return ans
