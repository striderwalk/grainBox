from grains import GRAINS


from consts import *
import pygame


class MouseHandler:
    def __init__(self):
        self.cursor_size = 1  # x by x square centered around the mouse cursor

        pygame.mouse.set_visible(False)
        self.current_type = None

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

    def update(self, win, box, current_type):

        self.draw_mouse(win)
        self.process_mouse(box, current_type)

    def process_mouse(self, box, current_type):
        x, y = self.get_position()
        x, y = x + 2, y + 2

        box_size = int((self.cursor_size - 1) / 2)

        if x < 0 or y < 0 or x > GRID_WIDTH or y > GRID_HEIGHT:
            return

        if not (x != 0 or y != 0 or x != GRID_WIDTH + 2 or y != GRID_HEIGHT + 2):
            return

        if pygame.mouse.get_pressed()[0]:
            start = max(x - box_size, 0), min(y - box_size, GRID_HEIGHT - 1)
            end = max(x + box_size + 1, 0), min(y + box_size + 1, GRID_HEIGHT - 1)

            box.place_grains(start, end, current_type)


class Selection:
    def __init__(self):
        self.options = list(GRAINS)
        self.index = 0

    def next(self):
        self.index = (self.index + 1) % len(GRAINS)
        print(self.current_selection)

    @property
    def current_selection(self):
        return self.options[self.index]


class InputHandler:
    def __init__(self):
        self.mouse = MouseHandler()
        self.selection = Selection()

    def update(self, win, box):

        self.mouse.update(win, box, self.selection.current_selection)
        # handle events -------------------------------->
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    box.reset()

                elif event.key == pygame.K_f:
                    box.check_chunks()
                elif event.key == pygame.K_SPACE:
                    self.selection.next()

            elif event.type == pygame.MOUSEWHEEL:
                self.mouse.scale_cursor(event.precise_y)
