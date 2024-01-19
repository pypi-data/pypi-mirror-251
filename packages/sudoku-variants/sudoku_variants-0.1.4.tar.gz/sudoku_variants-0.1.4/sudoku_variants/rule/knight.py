from typing import List

from sudoku_variants.rule.interface import Rule
from sudoku_variants.sudoku_const import DIGITS


class Knight(Rule):
    knight_moves = (
        (-2, 1),
        (-1, 2),
        (1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2),
        (-2, -1),
    )

    def check_move(self, board: List[List[int]], row: int, col: int, digit: int) -> bool:
        if digit not in DIGITS:
            return True

        for m in self.knight_moves:
            if (0 <= row + m[0] < len(board)) and (0 <= col + m[1] < len(board[0])):
                knight_digit = board[row + m[0]][col + m[1]]
                if digit == knight_digit:
                    return False

        return True
