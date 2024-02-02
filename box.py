import random
from copy import deepcopy


import numpy as np
import pygame

from consts import *
from grains import GRAIN_DATA, GRAINS


class BoxSimulator:
    def __init__(self):
        self.grid = np.array(
            [
                [GRAINS["water"] for _ in range(GRID_HEIGHT + 2)]
                for _ in range(GRID_WIDTH + 2)
            ]
        )
        chucks_width = int(np.ceil(GRID_WIDTH / CHUNK_SIZE))
        chucks_height = int(np.ceil(GRID_HEIGHT / CHUNK_SIZE))

        self.chunks = np.array(
            ([[2 for _ in range(chucks_height)] for _ in range(chucks_width)])
        )

    def check_chunks(self):
        for i in range(len(self.chunks)):
            for j in range(len(self.chunks[i])):
                chunk = self.grid[
                    i * CHUNK_SIZE
                    + 1 : min(i * CHUNK_SIZE + CHUNK_SIZE + 1, len(self.grid) - 1),
                    j * CHUNK_SIZE
                    + 1 : min(j * CHUNK_SIZE + CHUNK_SIZE + 1, len(self.grid[0]) - 1),
                ]

                if (chunk == GRAINS["air"]).all():
                    self.chunks[i, j] = 0

                else:
                    self.chunks[i, j] = 5

    def draw(self, win):
        for i_chunk in range(len(self.chunks)):
            for j_chunk in range(len(self.chunks[i_chunk])):
                if self.chunks[i_chunk, j_chunk] == 0:
                    continue

                start_i = max(1, i_chunk * CHUNK_SIZE - 1)
                end_i = min(start_i + CHUNK_SIZE + 1, len(self.grid) - 1)
                start_j = max(1, j_chunk * CHUNK_SIZE - 1)
                end_j = min(start_j + CHUNK_SIZE + 1, len(self.grid[0]) - 1)

                for i in range(start_i, end_i):
                    for j in range(start_j, end_j):
                        pygame.draw.rect(
                            win,
                            GRAIN_DATA[self.grid[i, j]][0],
                            (
                                (i - 1) * GRAIN_SIZE,
                                (j - 1) * GRAIN_SIZE,
                                GRAIN_SIZE,
                                GRAIN_SIZE,
                            ),
                        )

    def update_item(self, i, j, next_grid):
        if self.grid[i, j] == GRAINS["air"]:
            return

        # this = grid[i, j]
        this_data = GRAIN_DATA[self.grid[i, j]]

        neighborhood = self.grid[i - 1 : i + 2, j - 1 : j + 2]
        # if (neighborhood == this).all():
        # return
        moves = {}
        for i_offset in range(0, 3):
            for j_offset in range(0, 3):
                if this_data[1][i_offset, j_offset] == 0:
                    continue

                if this_data[2] <= GRAIN_DATA[neighborhood[i_offset, j_offset]][2]:
                    continue
                if (
                    this_data[2]
                    <= GRAIN_DATA[next_grid[i + i_offset - 1, j + j_offset - 1]][2]
                ):
                    continue
                moves[(i_offset - 1, j_offset - 1)] = this_data[1][i_offset, j_offset]

        if moves:
            max_value = max(moves.values())
            max_keys = [key for key, value in moves.items() if value == max_value]

            # i_offset, j_offset = max_keys[0]
            i_offset, j_offset = random.choice(max_keys)

            new_i = i + i_offset
            new_j = j + j_offset

            if new_i < 1 or new_i > len(self.grid) - 2:
                return False
            if new_j < 1 or new_j > len(self.grid[0]) - 2:
                return False

            next_grid[new_i, new_j] = next_grid[i, j]
            next_grid[i, j] = self.grid[new_i, new_j]

            self.chunks[int((new_i / CHUNK_SIZE)), int((new_j / CHUNK_SIZE))] = 5

            return True

    def update_grid(self):
        next_grid = deepcopy(self.grid)

        # Iterate over each chunk -------------------------------->
        for i_chunk in range(len(self.chunks)):
            for j_chunk in range(len(self.chunks[i_chunk])):

                if self.chunks[i_chunk, j_chunk] == 0:
                    continue

                # find real range chunk
                start_i = max(1, i_chunk * CHUNK_SIZE - 1)
                end_i = min(start_i + CHUNK_SIZE + 1, len(self.grid) - 1)

                start_j = max(1, j_chunk * CHUNK_SIZE - 1)
                end_j = min(start_j + CHUNK_SIZE + 1, len(self.grid[0]) - 1)

                # pick the direction to iterate
                i_range = (
                    range(start_i, end_i)
                    if random.random() < 0.5
                    else range(end_i - 1, start_i - 1, -1)
                )

                j_range = (
                    range(start_j, end_j)
                    if random.random() < 0.5
                    else range(end_j - 1, start_j - 1, -1)
                )

                change = False
                for i in i_range:
                    for j in j_range:

                        change = self.update_item(i, j, next_grid) or change

                if not change and self.chunks[i_chunk, j_chunk] > 0:
                    self.chunks[i_chunk, j_chunk] -= 1
                else:
                    if i_chunk > 0:
                        self.chunks[i_chunk - 1, j_chunk] = 5
                    if i_chunk < len(self.chunks) - 1:

                        self.chunks[i_chunk + 1, j_chunk] = 5

        self.grid = next_grid

    def place_grain(self, pos, grain):
        self.grid[pos] = grain

        self.chunks[int((pos[0] / CHUNK_SIZE)), int((pos[1] / CHUNK_SIZE))] = 5

    def place_grains(self, start_pos, end_pos, grain, keep=False):
        if not keep:
            self.grid[start_pos[0] : end_pos[0], start_pos[1] : end_pos[1]] = grain

        for i in range(start_pos[0], end_pos[0]):
            for j in range(start_pos[1], end_pos[1]):
                if GRAIN_DATA[self.grid[i, j]][2] < GRAIN_DATA[grain][2]:
                    self.grid[i, j] = grain

        # Turn on the chunks
        start_chunk = (start_pos[0] / CHUNK_SIZE), (start_pos[1] / CHUNK_SIZE)
        start_chunk = int(start_chunk[0]), int(start_chunk[1])

        end_chunk = (end_pos[0] / CHUNK_SIZE), (end_pos[1] / CHUNK_SIZE)
        end_chunk = int(end_chunk[0]), int(end_chunk[1])
        self.chunks[start_chunk] = 1
        self.chunks[end_chunk] = 1

        self.chunks[
            max(start_chunk[0] - 1, 0) : min(end_chunk[0] + 2, len(self.chunks)),
            max(start_chunk[1] - 1, 0) : min(end_chunk[1] + 2, len(self.chunks)),
        ] = 5


class Box:
    def __init__(self) -> None:
        self.simulatior = BoxSimulator()
        self.surface = pygame.Surface(
            (GRID_WIDTH * GRAIN_SIZE, GRID_HEIGHT * GRAIN_SIZE), flags=pygame.SRCALPHA
        )

        self.noise = pygame.Surface(
            ((GRID_WIDTH * GRAIN_SIZE, GRID_HEIGHT * GRAIN_SIZE))
        ).convert()  # flags=pygame.SRCALPHA)
        self.noise.set_alpha(50)
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                number = random.randint(25, 100)
                pygame.draw.rect(
                    self.noise,
                    (number, number, number),
                    (i * GRAIN_SIZE, j * GRAIN_SIZE, GRAIN_SIZE, GRAIN_SIZE),
                )

    def update(self, win):
        self.simulatior.update_grid()

        self.simulatior.draw(self.surface)
        win.blit(self.surface, (0, 0))
        win.blit(self.noise, (0, 0))

        self.draw_chunks(win)

    def draw_chunks(self, win):
        my_font = pygame.font.SysFont("Helvetica", 30)

        for i in range(len(self.simulatior.chunks)):
            for j in range(len(self.simulatior.chunks[i])):
                if self.simulatior.chunks[i, j] == 0:
                    continue
                text_surface = my_font.render(
                    str(self.simulatior.chunks[i, j]), False, WHITE
                )
                chunk_size = CHUNK_SIZE * GRAIN_SIZE
                win.blit(text_surface, ((i) * chunk_size, (j) * chunk_size))
                width = (
                    chunk_size
                    if (i) * chunk_size + chunk_size < GRAIN_SIZE * GRID_WIDTH
                    else -(i) * chunk_size + GRAIN_SIZE * GRID_WIDTH - 2
                )
                height = (
                    chunk_size
                    if (j) * chunk_size + chunk_size < GRAIN_SIZE * GRID_HEIGHT
                    else -(j) * chunk_size + GRAIN_SIZE * GRID_HEIGHT - 2
                )
                pygame.draw.rect(
                    win,
                    RED,
                    (
                        (i) * chunk_size,
                        (j) * chunk_size,
                        width,
                        height,
                    ),
                    width=1,
                )

    def place_grain(self, pos, grain):
        self.simulatior.place_grains(pos, grain)

    def place_grains(self, start_pos, end_pos, grain, **kwargs):
        self.simulatior.place_grains(start_pos, end_pos, grain, **kwargs)

    def reset(self):
        self.simulatior = BoxSimulator()

    def check_chunks(self):
        self.simulatior.check_chunks()
