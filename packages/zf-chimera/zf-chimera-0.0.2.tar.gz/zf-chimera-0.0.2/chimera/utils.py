from typing import List
from typing import Tuple

import numpy as np


def get_spiral_indices(r, c, x, y, n):
    def safe_append(safe_indices, n_r, n_c) -> List[Tuple[int, int]]:
        if 0 <= n_r < x and 0 <= n_c < y:
            safe_indices.append((n_r, n_c))
        return safe_indices

    row_start, row_end = r - 1, r + 1
    col_start, col_end = c - 1, c + 1

    # print(f"row_start: {row_start}")
    # print(f"row_end: {row_end}")
    # print(f"col_start: {col_start}")
    # print(f"col_end: {col_end}")

    row_curr = r - 1
    col_curr = c

    # print(f"row_curr: {row_curr}")
    # print(f"col_curr: {col_curr}")

    indices = []
    rounds = 0
    while rounds < n:
        # Go up
        while row_curr >= row_start:
            indices = safe_append(indices, row_curr, col_curr)
            row_curr -= 1
        row_curr += 1  # Undo the last decrement

        # print(f"after up: {indices}")

        # Go right
        col_curr += 1
        while col_curr <= col_end:
            indices = safe_append(indices, row_curr, col_curr)
            col_curr += 1
        col_curr -= 1
        row_curr += 1

        # print(f"after right: {indices}")

        # Go down
        while row_curr <= row_end:
            indices = safe_append(indices, row_curr, col_curr)
            row_curr += 1
        row_curr -= 1
        col_curr -= 1

        # print(f"after down: {indices}")

        # Go left
        while col_curr >= col_start:
            indices = safe_append(indices, row_curr, col_curr)
            col_curr -= 1
        col_curr += 1
        row_curr -= 1

        # print(f"after left: {indices}")

        # Go up
        while row_curr >= row_start:
            indices = safe_append(indices, row_curr, col_curr)
            row_curr -= 1

        # print(f"after up: {indices}")

        # Update the bounds
        row_start -= 1
        row_end += 1
        col_start -= 1
        col_end += 1

        # Increment the rounds
        rounds += 1

    return indices


def test_spiral_indices():
    x, y = 5, 5
    r, c = 1, 3
    indices = get_spiral_indices(r, c, x, y, n=10)
    print(f"indices: {indices}")

    mat = np.zeros((x, y))
    count = 1
    for i, j in indices:
        mat[i][j] = count
        count += 1
    print(mat)


if __name__ == "__main__":
    test_spiral_indices()
