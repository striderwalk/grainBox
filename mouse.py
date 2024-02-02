from consts import *
import pygame


class Mouse_hander:
    def __init__(self):
        self.cursor_size = 1  # x by x square centered around the mouse cursor

        pygame.mouse.set_visible(False)

    def scale_cursor(self, direction):
        self.cursor_size += 2 * direction

        self.cursor_size = max(self.cursor_size, 1)

    def get_position(self):
        x, y = pygame.mouse.get_pos()

        x /= GRAIN_SIZE
        y /= GRAIN_SIZE
        x = int(x) - 1
        y = int(y) - 1

        return x, y

    def _get_box_cords(self, x: float, y: float) -> tuple:
        # find topleft
        box_size = int((self.cursor_size - 1) / 2)
        topleft_x = (x - box_size) * GRAIN_SIZE
        topleft_y = (y - box_size) * GRAIN_SIZE

        box_cords = (
            topleft_x,
            topleft_y,
            self.cursor_size * GRAIN_SIZE,
            self.cursor_size * GRAIN_SIZE,
        )
        return box_cords

    def draw_mouse(self, win):
        if not pygame.mouse.get_focused():
            return

        x, y = self.get_position()
        x, y = x + 1, y + 1

        # draw centre

        w, h = GRAIN_SIZE, GRAIN_SIZE
        rect = (x * GRAIN_SIZE, y * GRAIN_SIZE, w, h)

        pygame.draw.rect(win, WHITE, rect)

        box_cords = self._get_box_cords(x, y)
        pygame.draw.rect(win, YELLOW, box_cords, width=1)

    def update(self, win, box):
        self.draw_mouse(win)
        self.process_mouse(box)

    def process_mouse(self, box):
        x, y = self.get_position()
        x, y = x + 2, y + 2

        box_size = int((self.cursor_size - 1) / 2)

        if x < 0 or y < 0 or x > GRID_SIZE or y > GRID_SIZE:
            return

        if pygame.mouse.get_pressed()[0]:
            if x != 0 or y != 0 or x != GRID_SIZE + 2 or y != GRID_SIZE + 2:
                box.place_grains(
                    (x - box_size, y - box_size),
                    (x + box_size + 1, y + box_size + 1),
                    "san",
                )

        elif pygame.mouse.get_pressed()[2]:
            if x != 0 or y != 0 or x != GRID_SIZE + 2 or y != GRID_SIZE + 2:
                box.place_grains(
                    (x - box_size, y - box_size),
                    (x + box_size + 1, y + box_size + 1),
                    "wat",
                )

        elif pygame.mouse.get_pressed()[1]:
            if x != 0 or y != 0 or x != GRID_SIZE + 2 or y != GRID_SIZE + 2:
                box.place_grains(
                    (x - box_size, y - box_size),
                    (x + box_size + 1, y + box_size + 1),
                    "stm",
                )
