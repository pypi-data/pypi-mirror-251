from typing import List

from sudoku_variants.rule.interface import Rule
from sudoku_variants.const import DIGITS, NUM_COL, NUM_ROW


class CenterDot(Rule):
    center_row = 1
    center_col = 1

    def description(self) -> str:
        return "Central cells in each 3x3 boxes contain all the numbers from 1 to 9 without repetition."

    def check_move(self, board: List[List[int]], row: int, col: int, digit: int) -> bool:
        if digit not in DIGITS:
            return True

        relative_row = row % 3
        relative_col = col % 3
        if (relative_row == self.center_row) and (relative_col == self.center_col):
            for i in range(NUM_ROW):
                cur_row = i // 3 * 3 + relative_row
                cur_col = i % 3 * 3 + relative_col
                cur_digit = board[cur_row][cur_col]
                if (cur_digit == digit) and ((cur_row != row) or (cur_col != col)):
                    return False

        return True
