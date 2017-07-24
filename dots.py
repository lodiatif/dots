import logging
from functools import wraps
from itertools import chain

import sys


def guide(game_grid, current_coord, destination_coord, threshold=2000):
    def northwest(f):
        @wraps(f)
        def wrapper(coordinate):
            idx = 1 if f.__name__ == 'left' else 0
            coordinate = list(coordinate)
            while coordinate[idx] > 0:
                coordinate[idx] -= 1
                if coordinate in steps:
                    if coordinate not in path:
                        return coordinate
                    elif coordinate != path[-2]:
                        continue
                    else:
                        raise Exception("Hop is restricted!")
            raise Exception("Move not possible!")

        return wrapper

    def southeast(f):
        @wraps(f)
        def wrapper(coordinate):
            idx = 1 if f.__name__ == 'right' else 0
            coordinate = list(coordinate)
            boundaries = (len(game_grid), len(game_grid[0]))

            while coordinate[idx] < boundaries[idx] - 1:
                coordinate[idx] += 1
                if coordinate in steps:
                    if coordinate not in path:
                        return coordinate
                    elif coordinate != path[-2]:
                        continue
                    else:
                        raise Exception("Hop is restricted!")
            raise Exception("Move not possible!")

        return wrapper

    @northwest
    def left(coordinate):
        pass

    @southeast
    def right(coordinate):
        pass

    @northwest
    def up(coordinate):
        pass

    @southeast
    def down(coordinate):
        pass

    cols = len(game_grid[0])
    steps = [[int(i / cols), i % cols] for i, e in enumerate(chain.from_iterable(game_grid)) if e == 1]

    counter = 0
    path = [current_coord, ]
    dark_paths = []
    while current_coord != destination_coord:
        moved = False
        for move in left, right, up, down:
            try:
                current_coord = move(current_coord)
                path.append(current_coord)
                if path in dark_paths:
                    log.debug("path already taken %s\n" % path)
                    path.pop()
                    current_coord = path[-1]
                    continue
                log.debug("Moved %s - %s\n" % (move.__name__, path))
                moved = True
                break
            except Exception as e:
                log.debug("%s - %s %s" % (current_coord, move.__name__, e))
        if not moved:
            log.debug("No move from %s, retreating.." % current_coord)
            dark_paths.append(list(path))
            path.pop()
            current_coord = path[-1]
        if current_coord == destination_coord and len(path) != len(steps):
            dark_paths.append(list(path))
            path.pop()
            current_coord = path[-1]
            log.debug("^  Wrong move from %s to destination %s, retreating..\n" % (current_coord, destination_coord))

        counter += 1
        if counter == threshold:
            log.warn("Couldn't complete within threshold (%s)" % threshold)
            break

    log.info("Last path %s" % path)


if __name__ == '__main__':
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    log.addHandler(ch)
    # TODO - resource hungry, optimise.
    game_grid = [[1, 1, 1, 1, 1], [1, 0, 0, 1, 1], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [1, 1, 0, 1, 1]]
    # game_grid = [[1, 1, 1, 0, 1], [0, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]]
    # game_grid = [[1, 1, 0, 0, 0], [1, 0, 0, 0, 1], [1, 0, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1]]
    # game_grid = [[0, 1, 1, 0, 0], [1, 0, 1, 0, 1], [0, 0, 1, 0, 1], [0, 0, 1, 0, 1], [1, 1, 1, 1, 1]]
    # game_grid = [[0, 1, 1, 0, 0], [0, 1, 1, 1, 1], [1, 1, 1, 0, 0], [1, 1, 1, 1, 1]]
    start_coord = [3, 2]
    destination_coord = [0, 4]

    guide(game_grid, start_coord, destination_coord)
