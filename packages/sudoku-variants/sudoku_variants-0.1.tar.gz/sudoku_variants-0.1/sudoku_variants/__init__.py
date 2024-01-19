import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / "..").resolve()))
from sudoku import Sudoku
from sudoku_ai import SudokuAI
import sudoku_const as SudokuConst
