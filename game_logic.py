import grid_io as gr


def count_live_neighbors(grid: list[list[int]], row: int, col: int) -> int:
    """
    Counts the number of live neighbors (cells with value 1)
    around a given cell in the grid.

    The function checks all 8 surrounding cells and ignores
    cells outside the grid boundaries.

    :param grid: 2D list representing the grid
    :param row: row index of the target cell
    :param col: column index of the target cell
    :return: number of live neighboring cells
    """
    counter = 0
    rows = len(grid)
    cols = len(grid[0])

    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < rows and 0 <= j < cols:
                if (i, j) != (row, col) and grid[i][j] == 1:
                    counter += 1
    return counter


def next_generation(grid: list[list[int]]) -> list[list[int]]:
    """
    Computes the next generation of the grid based on
    Conway's Game of Life rules.

    Rules:
    - A live cell (1) survives if it has 2 or 3 neighbors
    - A dead cell (0) becomes alive if it has exactly 3 neighbors
    - In all other cases, the cell becomes or remains dead

    :param grid: current generation grid
    :return: new grid representing the next generation
    """
    grid_return = gr.create_empty_grid(len(grid), len(grid[0]))

    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            neighbs = count_live_neighbors(grid, i, j)

            if grid[i][j] == 1 and (neighbs == 2 or neighbs == 3):
                grid_return[i][j] = 1
            elif grid[i][j] == 0 and neighbs == 3:
                grid_return[i][j] = 1
            else:
                grid_return[i][j] = 0

    return grid_return


def apply_boundary_condition(grid: list[list[int]], row: int, col: int) -> tuple[int, int]:
    """
    Applies periodic (toroidal) boundary conditions to coordinates.

    If the indices go beyond the grid boundaries, they wrap around
    to the opposite side of the grid.

    Example:
    - row = -1 -> last row
    - col = cols -> first column

    :param grid: 2D list representing the grid
    :param row: row index (can be out of bounds)
    :param col: column index (can be out of bounds)
    :return: tuple of valid (row, col) indices within the grid
    """
    rows = len(grid)
    cols = len(grid[0])

    return (row % rows, col % cols)
