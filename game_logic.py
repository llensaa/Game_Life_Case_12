import grid_io as gr


def count_live_neighbors(grid: list[list[int]], row: int, col: int) -> int:
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
    rows = len(grid)
    cols = len(grid[0])

    return (row % rows, col % cols)
