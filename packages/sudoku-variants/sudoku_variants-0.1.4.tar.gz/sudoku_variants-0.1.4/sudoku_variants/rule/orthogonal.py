from typing import List

from sudoku_variants.rule.interface import Rule
from sudoku_variants.sudoku_const import DIGITS, NUM_COL, NUM_ROW


class Orthogonal(Rule):
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

    def remove_candidates(
        self, candidates: List[List[List[bool]]], row: int, col: int, digit: int
    ) -> List[List[List[bool]]]:
        if digit in DIGITS:
            for col_index in range(NUM_COL):
                if col_index != col:
                    candidates[row][col_index][digit - 1] = False

            for row_index in range(NUM_ROW):
                if row_index != row:
                    candidates[row_index][col][digit - 1] = False

            candidates[row][col] = [False for _ in range(len(DIGITS))]

        return candidates
