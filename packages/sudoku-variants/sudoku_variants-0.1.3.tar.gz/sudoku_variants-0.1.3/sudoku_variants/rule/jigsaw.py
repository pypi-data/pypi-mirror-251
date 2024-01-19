import random

from typing import List, Tuple, Optional, Dict, Set

from sudoku_variants.rule.interface import Rule, WithData
from sudoku_variants.sudoku_const import DIGITS, NUM_COL, NUM_ROW

JigsawDataType = List[List[int]]
JigsawPartitionType = Dict[int, List[Tuple[int, int]]]


def _default_jigsaw_layout():
    return [[row // 3 * 3 + col // 3 for col in range(NUM_COL)] for row in range(NUM_ROW)]


class Jigsaw(Rule, WithData):
    def __init__(self, data: Optional[JigsawDataType] = None) -> None:
        """
        data: a 2D board, where each cell indicates the index of its partition
        """
        super().__init__()
        self.data: JigsawDataType
        if data is None:
            self.data = _default_jigsaw_layout()
        else:
            self.data = data

        # to retrive all coords in a partition quicker
        self.partition: JigsawPartitionType = {}
        for i, row in enumerate(self.data):
            for j, partition in enumerate(row):
                self.partition.setdefault(partition, [])
                self.partition[partition].append((i, j))

    def check_move(self, board: List[List[int]], row: int, col: int, digit: int) -> bool:
        if digit not in DIGITS:
            return True

        partiton = self.data[row][col]
        coords_in_partition = self.partition[partiton]
        for coord in coords_in_partition:
            if (board[coord[0]][coord[1]] == digit) and (coord != (row, col)):
                return False

        return True

    def populate_initial_data(self, seed: Optional[int] = None):
        # reference: https://softwareengineering.stackexchange.com/questions/419048/algorithm-to-split-a-grid-of-squares-into-equally-sized-sections
        random.seed(seed)

        data = _default_jigsaw_layout()
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def init_cell() -> Tuple[Tuple[int, int], int]:
            row = random.randint(0, len(data) - 1)
            col = random.randint(0, len(data[0]) - 1)
            coord = (row, col)
            partition = data[row][col]
            return (coord, partition)

        def is_partition_connected(partition: int) -> bool:
            coords: List[Tuple[int, int]] = []
            for i, row in enumerate(data):
                for j, p in enumerate(row):
                    if p == partition:
                        coords.append((i, j))
            size = len(coords)

            component: List[Tuple[int, int]] = [coords.pop()]
            has_new_coord = True
            while has_new_coord:
                has_new_coord = False
                new_coords: Set[Tuple[int, int]] = set()
                for coord in coords:
                    for offset in offsets:
                        neighbour = (coord[0] + offset[0], coord[1] + offset[1])
                        if neighbour in component:
                            new_coords.add(coord)

                if new_coords:
                    has_new_coord = True
                    component += new_coords
                    for c in new_coords:
                        coords.remove(c)

            return len(component) == size

        max_attempts = 300
        for i in range(max_attempts):
            coord1, partition1 = init_cell()
            coord2, partition2 = init_cell()
            data[coord1[0]][coord1[1]] = partition2
            data[coord2[0]][coord2[1]] = partition1

            is_data_connected = (
                (partition1 != partition2) and is_partition_connected(partition1) and is_partition_connected(partition2)
            )

            if not is_data_connected:
                data[coord1[0]][coord1[1]] = partition1
                data[coord2[0]][coord2[1]] = partition2

        self.data = data
        self.partition = {}
        for i, row in enumerate(self.data):
            for j, partition in enumerate(row):
                self.partition.setdefault(partition, [])
                self.partition[partition].append((i, j))

    def extract_data_from_board(self, board: List[List[int]]):
        pass
