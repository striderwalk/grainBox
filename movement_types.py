import random
from consts import GRID_HEIGHT, GRID_WIDTH
from grains import GRAIN_DATA


def can_move_down(current_density, new_i, new_j, grid, next_grid):

    return (
        current_density > GRAIN_DATA[grid[new_i, new_j]]["density"]
        and current_density > GRAIN_DATA[next_grid[new_i, new_j]]["density"]
        and GRAIN_DATA[grid[new_i, new_j]]["can_move"]
    )


def can_move_up(current_density, new_i, new_j, grid, next_grid):
    return (
        current_density < GRAIN_DATA[grid[new_i, new_j]]["density"]
        and current_density < GRAIN_DATA[next_grid[new_i, new_j]]["density"]
        and GRAIN_DATA[grid[new_i, new_j]]["can_move"]
    )


def move_solid(i: int, j: int, grid, next_grid) -> tuple:

    this_data = GRAIN_DATA[grid[i, j]]
    density = this_data["density"]
    # move down

    if can_move_down(density, i, j + 1, grid, next_grid):
        return (i, j + 1)

    # move across
    moves = []

    if can_move_down(density, i + 1, j + 1, grid, next_grid):

        moves.append((i + 1, j + 1))

    if can_move_down(density, i - 1, j + 1, grid, next_grid):

        if j + 1 < GRID_HEIGHT:
            moves.append((i - 1, j + 1))
    if moves:

        return random.choice(moves)


def move_liquid(i: int, j: int, grid, next_grid) -> tuple:

    this_data = GRAIN_DATA[grid[i, j]]
    density = this_data["density"]

    # move down

    if can_move_down(density, i, j + 1, grid, next_grid):

        return (i, j + 1)

    # move across
    moves = []

    if can_move_down(density, i + 1, j + 1, grid, next_grid):

        if density > GRAIN_DATA[grid[i + 1, j]]["density"]:
            if density > GRAIN_DATA[next_grid[i + 1, j]]["density"]:

                moves.append((i + 1, j + 1))

    if can_move_down(density, i - 1, j + 1, grid, next_grid):

        if density > GRAIN_DATA[grid[i - 1, j]]["density"]:
            if density > GRAIN_DATA[next_grid[i - 1, j]]["density"]:

                moves.append((i - 1, j + 1))

    if moves:

        return random.choice(moves)

    right, left = True, True
    for offset in range(1, this_data["viscosity"]):
        if i + offset > GRID_WIDTH:
            right = False
        if right:
            if can_move_down(density, i + offset, j, grid, next_grid):

                moves.append((i + offset, j))
            else:
                right = False

        if i - offset < 2:
            left = False
        if left:
            if can_move_down(density, i - offset, j, grid, next_grid):

                moves.append((i - offset, j))

            else:
                left = False
    if moves:

        return random.choice(moves)


def move_gas(i: int, j: int, grid, next_grid) -> tuple:

    this_data = GRAIN_DATA[grid[i, j]]
    density = this_data["density"]

    # move down

    if can_move_up(density, i, j - 1, grid, next_grid):

        return (i, j - 1)

    # move across
    moves = []

    if can_move_up(density, i + 1, j - 1, grid, next_grid):
        if can_move_up(density, i + 1, j, grid, next_grid):

            moves.append((i + 1, j - 1))

    if can_move_up(density, i - 1, j - 1, grid, next_grid):

        if can_move_up(density, i - 1, j, grid, next_grid):

            moves.append((i - 1, j - 1))

    if moves:

        return random.choice(moves)

    right, left = True, True
    for offset in range(1, this_data["viscosity"]):
        if i + offset > GRID_WIDTH:
            right = False
        if right:
            if can_move_up(density, i + offset, j, grid, next_grid):

                moves.append((i + offset, j))
            else:
                right = False

        if i - offset < 2:
            left = False
        if left:
            if can_move_up(density, i - offset, j, grid, next_grid):

                moves.append((i - offset, j))

            else:
                left = False

    if moves:

        return random.choice(moves)
