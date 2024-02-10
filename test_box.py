import multiprocessing
import random
import numpy as np


def box(grid):
    i, j = random.randint(0, len(grid)), random.randint(0, len(grid[0]))
    grid[i, j] = random.randint(0, 100)
    return grid


def update_box(send_queue, recive_queue):
    grid = np.zeros((5, 5))

    while True:
        if not recive_queue.empty():
            print("")
        grid = box(grid)
        send_queue.put(grid)


def main():
    send_queue = multiprocessing.Queue()
    recive_queue = multiprocessing.Queue()

    box_proccess = multiprocessing.Process(
        target=update_box, args=(send_queue, recive_queue)
    )

    box_proccess.start()
    for i in range(5):
        if not recive_queue.empty():
            print(send_queue.get())
        recive_queue.put("hi")
    box_proccess.terminate()


if __name__ == "__main__":
    main()
