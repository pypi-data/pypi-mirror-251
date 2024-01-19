from typing import List

from sudoku_variants.rule.interface import Rule, WithData
from sudoku_variants.rule.jigsaw import Jigsaw
from sudoku_variants.rule.orthogonal import Orthogonal
from sudoku_variants.rule.sub_board import SubBoard

# because Python doesn't have extension


def to_name(rules: List[Rule]):
    return ", ".join(str(r) for r in rules)


def check_move(rules: List[Rule], board: List[List[int]], row: int, col: int, digit: int) -> bool:
    return all(rule.check_move(board, row, col, digit) for rule in rules)


def remove_candidates(
    rules: List[Rule], candidates: List[List[List[bool]]], row: int, col: int, digit: int
) -> List[List[List[bool]]]:
    for rule in rules:
        candidates = rule.remove_candidates(candidates, row, col, digit)
    return candidates


def populate_initial_data(rules: List[Rule]):
    for rule in rules:
        if isinstance(rule, WithData):
            rule.populate_initial_data()


def extract_data_from_board(rules: List[Rule], board: List[List[int]]):
    for rule in rules:
        if isinstance(rule, WithData):
            rule.extract_data_from_board(board)


def with_standard_rules(rules: List[Rule]) -> List[Rule]:
    include_orthogonal = True
    include_sub_board = True
    for rule in rules:
        if isinstance(rule, Jigsaw) or isinstance(rule, SubBoard):
            include_sub_board = False
        elif isinstance(rule, Orthogonal):
            include_orthogonal = False

    if include_orthogonal:
        rules.append(Orthogonal())
    if include_sub_board:
        rules.append(SubBoard())

    return rules
