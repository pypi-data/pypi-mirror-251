from typing import List

from sudoku_variants.sudoku_const import DIGITS, NUM_COL, NUM_ROW
from sudoku_variants.rule.interface import Rule
from sudoku_variants.func import board as B, rules as R


class Sudoku:
    def __init__(self, board: List[List[int]], rules: List[Rule]) -> None:
        """
        Create a sudoku puzzle with board and rules. The puzzle can be potentially invalid.

        Args:
            board: sudoku board
            rules: types of rule to be applied to this puzzle

        Returns:
            A new Sudoku

        Raises:
            TypeError: when the shape of board is not expected
        """
        board_shape = B.shape_of_board(board)
        expected_shape = (NUM_ROW, NUM_COL)
        if board_shape != expected_shape:
            raise TypeError(f"Expect board to have shape {expected_shape}, got {board_shape}")

        self.board = board
        self.rules = rules

    def check_move(self, row, col, digit) -> bool:
        return R.check_move(self.rules, self.board, row, col, digit)

    def check_board(self) -> bool:
        board = [[0 for _ in range(NUM_COL)] for _ in range(NUM_ROW)]
        empty_sudoku = Sudoku(board, self.rules)
        for row in range(NUM_ROW):
            for col in range(NUM_COL):
                digit = self.board[row][col]
                if not empty_sudoku.check_move(row, col, digit):
                    return False
                empty_sudoku.board[row][col] = digit

        return True

    def __str__(self) -> str:
        textRows = []
        sepLine = (
            "+"
            + "-" * (NUM_COL // 3 * 2 + 1)
            + "+"
            + "-" * (NUM_COL // 3 * 2 + 1)
            + "+"
            + "-" * (NUM_COL // 3 * 2 + 1)
            + "+"
        )

        textRows.append(f"Rules: {R.to_name(self.rules)}")
        textRows.append(sepLine)
        for i, row in enumerate(self.board):
            chars = ["|"]
            for j, digit in enumerate(row):
                chars.append(str(digit) if digit in DIGITS else "*")
                if j in [2, 5, 8]:
                    chars.append("|")
            textRows.append(" ".join(chars))

            if i in [2, 5, 8]:
                textRows.append(sepLine)

        return "\n".join(textRows)

    def copy(self) -> "Sudoku":
        return Sudoku(B.copy_board(self.board), self.rules)
