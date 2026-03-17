import random as r


def create_empty_grid(rows: int, cols: int) -> list[list[int]]:
    list_return = []
    for row in range(rows):
        row_list = [0 for _ in range(cols)]
        list_return.append(row_list)
    return list_return


def random_grid(rows: int, cols: int, prob: float = 0.5) -> list[list[int]]:
    list_return = []
    for row in range(rows):
        row_list = [0 if r.random() < prob else 1 for _ in range(cols)]
        list_return.append(row_list)
    return list_return


def load_grid_from_file(filename: str) -> list[list[int]]:
    list_return = []
    with open(f'{filename}', 'r') as f:
        for line in f:
            line = line.strip()
            list_return.append([int(x) for x in line])
    return list_return


def save_grid_to_file(grid: list[list[int]], filename: str) -> None:
    with open(f'{filename}', 'w') as f:
        for row in grid:
            f.write(''.join(str(x) for x in row) + '\n')


def set_cell(grid: list[list[int]], row: int, col: int, value: int) -> None:
    if 0 <= row < len(grid) and 0 <= col < len(grid[row]):
        grid[row][col] = value
    else:
        raise IndexError("Row or column out of range")
