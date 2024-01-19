from typing import List

from sudoku_variants.rule.interface import Rule
from sudoku_variants.sudoku_const import DIGITS


class King(Rule):
    king_moves = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )

    def check_move(self, board: List[List[int]], row: int, col: int, digit: int) -> bool:
        if digit not in DIGITS:
            return True

        for m in self.king_moves:
            if (0 <= row + m[0] < len(board)) and (0 <= col + m[1] < len(board[0])):
                king_digit = board[row + m[0]][col + m[1]]
                if digit == king_digit:
                    return False

        return True
