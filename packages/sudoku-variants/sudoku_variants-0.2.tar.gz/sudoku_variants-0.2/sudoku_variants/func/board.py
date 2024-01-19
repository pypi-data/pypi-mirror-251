from typing import List, TypeVar, Tuple


T = TypeVar("T")


def shape_of_board(board: List[List]) -> Tuple[int, int]:
    return len(board), len(board[0])


def copy_board(board: List[List[T]]) -> List[List[T]]:
    return [[d for d in row] for row in board]
