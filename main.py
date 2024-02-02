import pygame

from box import Box
from consts import *
from inputs import InputHandler


def main():
    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # setup grid
    box = Box()
    box.place_grains((10, 50), (30, 74), "air")
    input_handler = InputHandler()

    # main loop -------------------------------->
    # for i in range(1000):
    while True:
        box.update(win)
        if input_handler.update(win, box):
            pygame.quit()
            return

        # update frame
        pygame.display.flip()
        win.fill(WHITE)
        clock.tick(FPS)
        cur_fps = clock.get_fps()
        fps_text = f"FPS: {cur_fps:.2f}"
        pygame.display.set_caption(fps_text)  # Set window title to display FPS


if __name__ == "__main__":
    main()
