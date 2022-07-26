import time

from grid import Grid
from typing import Optional


def _is_cell_valid(grid: Grid, row: int, column: int, value: int) -> bool:
    for i in range(9):
        if i != row and grid.get_number(i, column) == value:  # already the same value in the column
            return False
        if i != column and grid.get_number(row, i) == value:  # already the same value in the row
            return False

    # The grid is made of 9 regions with 3x3 cells
    region_x = row // 3
    region_y = column // 3
    for dx in range(3):
        for dy in range(3):
            x, y = region_x * 3 + dx, region_y * 3 + dy
            if x != row and y != column and grid.get_number(x, y) == value:  # already the same value in the same region
                return False

    return True


def _is_grid_filled(grid: Grid):
    for row in range(9):
        for column in range(9):
            if not grid.get_number(row, column):
                return False

    return True


def _get_candidate_numbers(grid: Grid, row: int, column: int):
    candidates = set()

    for i in range(1, 10):
        if _is_cell_valid(grid, row, column, i):
            candidates.add(i)

    return candidates


def solve(grid: Grid, sleep_time=0) -> bool:
    if sleep_time:
        time.sleep(sleep_time)

    if _is_grid_filled(grid):
        return True

    for row in range(9):
        for col in range(9):
            if not grid.get_number(row, col):  # cell is empty
                # Try all valid values for this cell
                for candidate in _get_candidate_numbers(grid, row, col):
                    grid.set_number(row, col, candidate)
                    has_solution = solve(grid, sleep_time)
                    if has_solution:
                        return True

                    # Invalid state, backtrack
                    grid.empty_cell(row, col)

                return False
