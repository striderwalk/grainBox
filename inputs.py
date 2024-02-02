from grains import GRAINS


from consts import *
import pygame


class MouseHandler:
    def __init__(self):
        self.cursor_size = 1  # x by x square centered around the mouse cursor

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

    def _get_placement_cords(self, x, y):
        box_size = int((self.cursor_size - 1) / 2)
        topleft_x = max((x - box_size), 1)
        topleft_y = max((y - box_size), 1)
        bottomright_x = min(x + box_size + 1, GRID_WIDTH + 1)
        bottomright_y = min(y + box_size + 1, GRID_HEIGHT + 1)
        return (topleft_x, topleft_y), (bottomright_x, bottomright_y)

    def _get_box_cords(self, x: float, y: float) -> tuple:
        # find topleft
        box_size = int((self.cursor_size - 1) / 2)
        topleft_x = max((x - box_size) * GRAIN_SIZE, 1)
        topleft_y = max((y - box_size) * GRAIN_SIZE, 1)

        size = self.cursor_size * GRAIN_SIZE

        width = (
            size
            if topleft_x + size < GRAIN_SIZE * GRID_WIDTH
            else -topleft_x + GRAIN_SIZE * GRID_WIDTH - 2
        )
        height = (
            size
            if topleft_y + size < GRAIN_SIZE * GRID_HEIGHT
            else -topleft_y + GRAIN_SIZE * GRID_HEIGHT - 2
        )
        box_cords = (topleft_x, topleft_y, width, height)
        return box_cords

    def draw_mouse(self, win):

        x, y = self.get_position()
        x, y = x + 1, y + 1
        if x < 0 or y < 0 or x > GRID_WIDTH or y > GRID_HEIGHT:
            pygame.mouse.set_visible(True)
            return
        else:
            pygame.mouse.set_visible(False)
        if not pygame.mouse.get_focused():
            return

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

        if x < 0 or y < 0 or x > GRID_WIDTH or y > GRID_HEIGHT:
            return

        if pygame.mouse.get_pressed()[0]:
            start, end = self._get_placement_cords(x, y)

            box.place_grains(start, end, current_type)


class Selection:
    def __init__(self):

        self.grains = list(GRAINS.values())
        self.grain_to_name = {value: key for key, value in GRAINS.items()}

        self.index = 0

    def next(self):
        self.index = (self.index + 1) % len(self.grains)

    @property
    def current_selection_name(self):
        return self.grain_to_name[self.current_selection]

    @property
    def current_selection(self):
        return self.grains[self.index]


class InputHandler:
    def __init__(self):
        self.mouse = MouseHandler()
        self.selection = Selection()

    def update(self, win, box):
        my_font = pygame.font.SysFont("Helvetica", 30)
        win.blit(
            my_font.render(self.selection.current_selection_name, False, WHITE),
            (10, 10),
        )
        self.mouse.update(win, box, self.selection.current_selection)
        # handle events -------------------------------->
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    box.reset()
                elif event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_f:
                    box.check_chunks()
                elif event.key == pygame.K_SPACE:
                    self.selection.next()

            elif event.type == pygame.MOUSEWHEEL:
                self.mouse.scale_cursor(event.precise_y)
