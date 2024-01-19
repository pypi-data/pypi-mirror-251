from typing import List

from sudoku_variants.rule.interface import Rule
from sudoku_variants.const import DIGITS, NUM_COL, NUM_ROW


class Orthogonal(Rule):
    def description(self) -> str:
        return "Each column and each row contains all the numbers from 1 to 9 without repetition."

    def check_move(self, board: List[List[int]], row: int, col: int, digit: int) -> bool:
        if digit not in DIGITS:
            return True

        for col_index in range(NUM_COL):
            cur_digit = board[row][col_index]
            if (cur_digit == digit) and (col_index != col):
                return False

        for row_index in range(NUM_ROW):
            cur_digit = board[row_index][col]
            if (cur_digit == digit) and (row_index != row):
                return False

        return True
