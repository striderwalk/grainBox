import random
import pygame

from consts import *
from grains import GRAIN_DATA
from simulator import BoxSimulator


class Box:
    def __init__(self) -> None:
        self.update_simulation = True

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

    def toggle_pause(self):
        self.update_simulation = not self.update_simulation

    def update(self, win):
        if self.update_simulation:
            self.simulatior.update_grid()
        self.draw_grid(self.surface)
        win.blit(self.surface, (0, 0))
        win.blit(self.noise, (0, 0))
        # if self.update_simulation:

        self.draw_chunks(win)

    def draw_grid(self, win):
        for i_chunk in range(len(self.simulatior.chunks)):
            for j_chunk in range(len(self.simulatior.chunks[i_chunk])):
                if self.simulatior.chunks[i_chunk, j_chunk] == 0:
                    continue

                start_i = max(1, i_chunk * CHUNK_SIZE - 1)
                end_i = min(start_i + CHUNK_SIZE + 1, GRID_WIDTH + 1)
                start_j = max(1, j_chunk * CHUNK_SIZE - 1)
                end_j = min(start_j + CHUNK_SIZE + 1, GRID_HEIGHT + 1)

                for i in range(start_i, end_i):
                    for j in range(start_j, end_j):
                        pygame.draw.rect(
                            win,
                            GRAIN_DATA[self.simulatior.grid[i, j]]["colour"],
                            (
                                (i - 1) * GRAIN_SIZE,
                                (j - 1) * GRAIN_SIZE,
                                GRAIN_SIZE,
                                GRAIN_SIZE,
                            ),
                        )

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
        self.simulatior.place_grain(pos, grain)

    def place_grains(self, start_pos, end_pos, grain, **kwargs):
        self.simulatior.place_grains(start_pos, end_pos, grain, **kwargs)

    def reset(self):
        self.simulatior = BoxSimulator()

    def check_chunks(self):
        self.simulatior.check_chunks()
