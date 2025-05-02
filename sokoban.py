from functools import cache
from heapq import heappop, heappush
from itertools import permutations, product
from sys import stdin


def main():
    grid = [line.rstrip() for line in stdin.readlines()]
    walls = set()
    goals = []
    initial_boxes = []
    height = len(grid)
    width = len(grid[0])
    previous = {}
    py = -1
    px = -1

    for y, x in product(range(height), range(width)):
        tile = grid[y][x]

        match tile:
            case '#':
                walls.add((y, x))
            case 'S':
                py, px = y, x
            case 'O':
                goals.append((y, x))
            case 'X':
                initial_boxes.append((y, x))

    initial_state = (tuple(sorted(initial_boxes)), py, px)

    @cache
    def distance(y1, x1, y2, x2):
        return abs(y2-y1) + abs(x2-x1)

    @cache
    def heuristic(boxes):
        best = 10**10

        for p in permutations(boxes):
            d = 0

            for i, b in enumerate(p):
                d += distance(b[0], b[1], goals[i][0], goals[i][1])

            best = min(best, d)

        return best
    
    def print_state(state):
        out = []
        boxes, sy, sx = state

        for y in range(height):
            row = []

            for x in range(width):
                if (y, x) in walls:
                    row.append('#')
                elif (y, x) in boxes:
                    row.append('X')
                elif (y, x) in goals:
                    row.append('O')
                elif (y, x) == (sy, sx):
                    row.append('S')
                else:
                    row.append('.')

            out.append(''.join(row))

        return '\n'.join(out)

    def pretty_print(state):
        out = []

        while True:
            out.append(print_state(state))

            if state not in previous:
                break

            state = previous[state]

        print('\n\n'.join(o for o in out[::-1]))

    @cache
    def get_moves(state):
        boxes, y, x = state

        moves = []
        frontier = [(y, x)]
        seen = {(y, x)}

        for fy, fx in frontier:
            print(fy, fx)
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):

                step = (fy+dy, fx+dx)

                if step in boxes:
                    behind = (fy+dy+dy, fx+dx+dx)

                    if behind not in boxes and behind not in walls:
                        dboxes = [box for box in boxes if box != step]
                        dboxes.append(behind)
                        moves.append((tuple(sorted(dboxes)), step[0], step[1]))
                elif step not in walls and step not in seen:
                    frontier.append((step[0], step[1]))
                    seen.add(step)

        return moves
    
    frontier = [(heuristic(tuple(initial_boxes)), 0, initial_state)]

    while frontier:
        ideal, steps, state = heappop(frontier)

        if ideal == steps:
            pretty_print(state)
            return
        
        for dstate in get_moves(state):
            if dstate in previous:
                continue
            
            dboxes = dstate[0]

            h = heuristic(dboxes)

            previous[dstate] = state
            heappush(frontier, (steps+h+1, steps+1, dstate))

if __name__ == '__main__':
    main()