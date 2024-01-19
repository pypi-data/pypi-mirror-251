import random
import sys

from typing import Tuple, Optional, List

from sudoku_variants.sudoku import Sudoku
from sudoku_variants.sudoku_const import DIGITS, NUM_COL, NUM_ROW
from sudoku_variants.rule.interface import Rule
from sudoku_variants.func import board as B, rules as R


class SudokuAI:
    @staticmethod
    def generate(
        rules: List[Rule],
        with_standard_rules: bool = True,
        max_erased: int = NUM_ROW * NUM_COL,
        mask: Optional[List[List[Optional[bool]]]] = None,
        timeout_solve: int = 5000,
        timeout_erase: int = 1000,
        seed: Optional[int] = None,
    ) -> Optional[Sudoku]:
        """
        Solve an empty sudoku given the rule types and populate data according to it
        """
        if with_standard_rules:
            rules = R.with_standard_rules(rules)
        R.populate_initial_data(rules)
        empty_board = [[0] * NUM_COL for _ in range(NUM_ROW)]

        board, _ = _solve_helper(empty_board, rules, timeout_solve, seed)
        if board is None:
            return None
        R.extract_data_from_board(rules, board)

        board = _erase_board_helper(
            board,
            rules,
            max_erased=max_erased,
            timeout=timeout_erase,
            seed=seed,
            mask=mask,
        )
        return Sudoku(board, rules)

    @staticmethod
    def solve(
        sudoku: Sudoku,
        timeout: int = sys.maxsize,
        seed: Optional[int] = None,
    ) -> Optional[Sudoku]:
        """
        Solve the given sudoku using DFS

        Args:
            sudoku: initial sudoku puzzle
            timeout: maximum time to solve
            seed: control the solve procedure
            on_new_progress: called everytime a new cell is filled. Accept the current proportion of filled cells as input

        Returns:
            a solved Sudoku or None if failed
        """
        solution, _ = _solve_helper(sudoku.board, sudoku.rules, timeout, seed)
        if solution is None:
            return None
        return Sudoku(solution, sudoku.rules)


def _get_first_empty_or_none(board: List[List[int]]):
    for i in range(NUM_ROW):
        for j in range(NUM_COL):
            if board[i][j] not in DIGITS:
                return (i, j)
    return None


def _init_candidates(board: Optional[List[List[int]]], rules: Optional[List[Rule]]) -> List[List[List[bool]]]:
    """
    True -> possible candidate; False -> impossible candidate
    """
    candidates = [[[True for _ in range(len(DIGITS))] for _ in range(NUM_COL)] for _ in range(NUM_ROW)]
    if (board is None) or (rules is None):
        return candidates

    for row in range(NUM_ROW):
        for col in range(NUM_COL):
            digit = board[row][col]
            candidates = R.remove_candidates(rules, candidates, row, col, digit)
    return candidates


def _solve_helper(
    board: List[List[int]],
    rules: List[Rule],
    timeout: int,
    seed: Optional[int],
) -> Tuple[Optional[List[List[int]]], List[List[List[int]]]]:
    """
    Return a tuple of a solved board or None and the remaining stacks
    """
    random.seed(seed)
    stacks = [board]

    while stacks:
        cur_board = stacks.pop()
        empty_cell = _get_first_empty_or_none(cur_board)

        if empty_cell is not None:
            digits = random.sample(DIGITS, len(DIGITS))
            for digit in digits:
                if R.check_move(rules, cur_board, empty_cell[0], empty_cell[1], digit):
                    new_board = B.copy_board(cur_board)
                    new_board[empty_cell[0]][empty_cell[1]] = digit
                    stacks.append(new_board)
        else:
            return cur_board, stacks

    return None, []


def _has_unique_solution_helper(
    board: List[List[int]],
    rules: List[Rule],
    seed: Optional[int],
) -> bool:
    solution, stacks = _solve_helper(board, rules, timeout=sys.maxsize, seed=seed)
    if solution == None:
        # there is no solution
        return False

    while stacks:
        cur_board = stacks.pop()
        cur_board, cur_stacks = _solve_helper(cur_board, rules, sys.maxsize, seed=seed)
        if cur_board is not None:
            # there is second solution
            return False

        stacks += cur_stacks

    return True


def _erase_board_helper(
    board: List[List[int]],
    rules: List[Rule],
    mask: Optional[List[List[Optional[bool]]]],
    max_erased: int,
    timeout: int,
    seed: Optional[int],
):
    random.seed(seed)
    cur_board = B.copy_board(board)

    if mask is None:
        mask = [[None for _ in range(NUM_COL)] for _ in range(NUM_ROW)]

    coords_to_erase: List[Tuple[int, int]] = []
    for i, row in enumerate(mask):
        for j, b in enumerate(row):
            # b -> None: potential cell to erase, -> False: always erase, -> True: always keep
            if b is None:
                coords_to_erase.append((i, j))
            elif not b:
                cur_board[i][j] = 0
    random.shuffle(coords_to_erase)
    # candidates = _init_candidates(cur_board, rules)
    # coords_to_erase.sort(key=lambda c: sum(candidates[c[0]][c[1]]))

    has_erase = True
    num_erase = 0
    for i, row in enumerate(cur_board):
        for j, d in enumerate(row):
            if d not in DIGITS:
                num_erase += 1

    while has_erase and num_erase < max_erased:
        has_erase = False

        checked_coords = []
        for i, j in coords_to_erase:
            if cur_board[i][j] in DIGITS:
                checked_coords.append((i, j))
                next_board = B.copy_board(cur_board)
                next_board[i][j] = 0
                is_unique = _has_unique_solution_helper(next_board, rules, seed=seed)
                if is_unique:
                    cur_board = next_board
                    has_erase = True
                    break

        # even if erasing this cell does not have unique solution now, we will never consider it either
        for c in checked_coords:
            coords_to_erase.remove(c)
        num_erase += 1

    return cur_board
