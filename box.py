import random
from copy import deepcopy


import numpy as np
import pygame

from consts import *
from grains import GRAIN_DATA


class BoxSimulator:
    def __init__(self):
        self.grid = np.array(
            [["air" for _ in range(GRID_SIZE + 2)] for _ in range(GRID_SIZE + 2)]
        )
        chucks = int(np.ceil(GRID_SIZE / CHUNK_SIZE))

        self.chunks = np.array(([[2 for _ in range(chucks)] for _ in range(chucks)]))

    def check_chunks(self):
        for i in range(len(self.chunks)):
            for j in range(len(self.chunks[i])):
                chunk = self.grid[
                    i * CHUNK_SIZE
                    + 1 : min(i * CHUNK_SIZE + CHUNK_SIZE + 1, len(self.grid) - 1),
                    j * CHUNK_SIZE
                    + 1 : min(j * CHUNK_SIZE + CHUNK_SIZE + 1, len(self.grid) - 1),
                ]

                if (chunk == "air").all():
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
                end_j = min(start_j + CHUNK_SIZE + 1, len(self.grid) - 1)

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
        if self.grid[i, j] == "air":
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
            if new_j < 1 or new_j > len(self.grid) - 2:
                return False

            next_grid[new_i, new_j] = next_grid[i, j]
            next_grid[i, j] = self.grid[new_i, new_j]

            self.chunks[int((new_i / CHUNK_SIZE)), int((new_j / CHUNK_SIZE))] = 5

            return True

    def update_grid(self):
        next_grid = deepcopy(self.grid)

        for i_chunk in range(len(self.chunks)):
            for j_chunk in range(len(self.chunks[i_chunk])):
                if self.chunks[i_chunk, j_chunk] == 0:
                    continue

                start_i = max(1, i_chunk * CHUNK_SIZE - 1)
                end_i = min(start_i + CHUNK_SIZE + 1, len(self.grid) - 1)

                start_j = max(1, j_chunk * CHUNK_SIZE - 1)
                end_j = min(start_j + CHUNK_SIZE + 1, len(self.grid) - 1)

                # pick the direction to iterate
                change = False
                # for i in range(start_i, end_i):
                #     for j in range(start_j, end_j):
                #         change = self.update_item(i, j, next_grid) or change
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

                for i in i_range:
                    for j in j_range:
                        change = self.update_item(i, j, next_grid) or change

                if not change:
                    self.chunks[i_chunk, j_chunk] -= 1
                    self.chunks[i_chunk, j_chunk] = max(
                        self.chunks[i_chunk, j_chunk], 0
                    )

        self.grid = next_grid

    def place_grain(self, pos, grain):
        self.grid[pos] = grain

        self.chunks[int((pos[0] / CHUNK_SIZE)), int((pos[1] / CHUNK_SIZE))] = 5

    def place_grains(self, start_pos, end_pos, grain):
        self.grid[start_pos[0] : end_pos[0], start_pos[1] : end_pos[1]] = grain

        self.chunks[
            int((start_pos[0] / CHUNK_SIZE)), int((start_pos[1] / CHUNK_SIZE))
        ] = 5
        self.chunks[int((end_pos[0] / CHUNK_SIZE)), int((end_pos[1] / CHUNK_SIZE))] = 5

    def reset(self):
        self.grid = np.array(
            [["air" for _ in range(GRID_SIZE + 2)] for _ in range(GRID_SIZE + 2)]
        )


class Box:
    def __init__(self) -> None:
        self.simulatior = BoxSimulator()
        self.surface = pygame.Surface((WIDTH, HEIGHT), flags=pygame.SRCALPHA)

        self.noise = pygame.Surface((WIDTH, HEIGHT)).convert()  # flags=pygame.SRCALPHA)
        self.noise.set_alpha(100)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                number = random.randint(0, 50)
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
                chunk_size = GRAIN_SIZE * CHUNK_SIZE
                win.blit(text_surface, ((i) * chunk_size, (j) * chunk_size))
                pygame.draw.rect(
                    win,
                    RED,
                    (
                        (i) * chunk_size,
                        (j) * chunk_size,
                        chunk_size,
                        chunk_size,
                    ),
                    width=1,
                )

    def place_grain(self, pos, grain):
        self.simulatior.place_grains(pos, grain)

    def place_grains(self, start_pos, end_pos, grain):
        self.simulatior.place_grains(start_pos, end_pos, grain)

    def reset(self):
        self.simulatior = BoxSimulator()

    def check_chunks(self):
        self.simulatior.check_chunks()
