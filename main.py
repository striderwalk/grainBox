import random

import pygame

from box import Box
from consts import *
from mouse import Mouse_hander


def main():
    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # setup grid
    box = Box()
    mouse_handler = Mouse_hander()

    box.place_grains((10, 50), (30, 74), "air")

    # main loop -------------------------------->

    for i in range(1000):
        # while True:
        box.update(win)
        mouse_handler.update(win, box)

        # handle events -------------------------------->
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    box.reset()

                elif event.key == pygame.K_f:
                    box.check_chunks()

            elif event.type == pygame.MOUSEWHEEL:
                mouse_handler.scale_cursor(event.precise_y)

        # update frame
        pygame.display.flip()
        win.fill(WHITE)
        clock.tick(FPS)
        cur_fps = clock.get_fps()
        fps_text = f"FPS: {cur_fps:.2f}"
        pygame.display.set_caption(fps_text)  # Set window title to display FPS


if __name__ == "__main__":
    main()
