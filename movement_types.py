import random
from grains import GRAIN_DATA


def move_solid(i: int, j: int, grid, next_grid) -> tuple:

    this_data = GRAIN_DATA[grid[i, j]]
    density = this_data["density"]
    # move down
    if density > GRAIN_DATA[grid[i, j + 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i, j + 1]]["density"]:
            if j + 1 < len(grid[0]) - 1:
                return (i, j + 1)

    # move across
    moves = []
    if density > GRAIN_DATA[grid[i + 1, j + 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i + 1, j + 1]]["density"]:
            if j + 1 < len(grid[0]) - 1:
                moves.append((i + 1, j + 1))

    if density > GRAIN_DATA[grid[i - 1, j + 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i - 1, j + 1]]["density"]:
            if j + 1 < len(grid[0]) - 1:
                moves.append((i - 1, j + 1))
    if moves:

        return random.choice(moves)


def move_liqud(i: int, j: int, grid, next_grid) -> tuple:

    this_data = GRAIN_DATA[grid[i, j]]
    density = this_data["density"]

    # move down
    if density > GRAIN_DATA[grid[i, j + 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i, j + 1]]["density"]:
            if j + 1 < len(grid[0]) - 1:
                return (i, j + 1)

    # move across
    moves = []
    if density > GRAIN_DATA[grid[i + 1, j + 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i + 1, j + 1]]["density"]:
            if j + 1 < len(grid[0]) - 1:
                if density > GRAIN_DATA[grid[i + 1, j]]["density"]:
                    if density > GRAIN_DATA[next_grid[i + 1, j]]["density"]:

                        moves.append((i + 1, j + 1))

    if density > GRAIN_DATA[grid[i - 1, j + 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i - 1, j + 1]]["density"]:
            if j + 1 < len(grid[0]) - 1:
                if density > GRAIN_DATA[grid[i - 1, j]]["density"]:
                    if density > GRAIN_DATA[next_grid[i - 1, j]]["density"]:

                        moves.append((i - 1, j + 1))

    if moves:

        return random.choice(moves)

    moves = []
    right, left = True, True
    for offset in range(1, this_data["viscosity"]):
        if i + offset > len(grid) - 2:
            right = False
        if right:
            if density > GRAIN_DATA[grid[i + offset, j]]["density"]:
                if density > GRAIN_DATA[next_grid[i + offset, j]]["density"]:
                    moves.append((i + offset, j))
                else:
                    right = False

            else:
                right = False

        if i - offset < 2:
            left = False
        if left:
            if density > GRAIN_DATA[grid[i - offset, j]]["density"]:
                if density > GRAIN_DATA[next_grid[i - offset, j]]["density"]:
                    moves.append((i - offset, j))
                else:
                    left = False

            else:
                left = False

    if moves:

        return random.choice(moves)


def move_gas(i: int, j: int, grid, next_grid) -> tuple:

    this_data = GRAIN_DATA[grid[i, j]]
    density = this_data["density"]

    # move down
    if density > GRAIN_DATA[grid[i, j - 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i, j - 1]]["density"]:
            if j - 1 > 1:
                return (i, j - 1)

    # move across
    moves = []
    if density > GRAIN_DATA[grid[i + 1, j - 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i + 1, j - 1]]["density"]:
            if j - 1 > 1:
                if density > GRAIN_DATA[grid[i + 1, j]]["density"]:
                    if density > GRAIN_DATA[next_grid[i + 1, j]]["density"]:
                        moves.append((i + 1, j - 1))

    if density > GRAIN_DATA[grid[i - 1, j - 1]]["density"]:
        if density > GRAIN_DATA[next_grid[i - 1, j - 1]]["density"]:
            if j - 1 > 1:
                if density > GRAIN_DATA[grid[i - 1, j]]["density"]:
                    if density > GRAIN_DATA[next_grid[i - 1, j]]["density"]:
                        moves.append((i - 1, j - 1))

    if moves:

        return random.choice(moves)

    moves = []
    right, left = True, True
    for offset in range(1, this_data["viscosity"]):
        if i + offset > len(grid) - 2:
            right = False
        if right:
            if density > GRAIN_DATA[grid[i + offset, j]]["density"]:
                if density > GRAIN_DATA[next_grid[i + offset, j]]["density"]:
                    moves.append((i + offset, j))
                else:
                    right = False

            else:
                right = False

        if i - offset < 2:
            left = False
        if left:
            if density > GRAIN_DATA[grid[i - offset, j]]["density"]:
                if density > GRAIN_DATA[next_grid[i - offset, j]]["density"]:
                    moves.append((i - offset, j))
                else:
                    left = False

            else:
                left = False

    if moves:

        return random.choice(moves)
