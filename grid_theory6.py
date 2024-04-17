#6.(5p) Allow wrapping around the grid. For example, from the last column you can step right and you get to the first column. It’s like some versions of Snake game.

import random
from collections import deque
import time
from copy import deepcopy



def dfs(grid, start_row, start_col, end_row, end_col, visited):
    if start_row < 0 or start_row >= len(grid) or start_col < 0 or start_col >= len(grid[0]) or grid[start_row][start_col] == '#' or (start_row, start_col) in visited:
        return False

    visited.add((start_row, start_col))

    if grid[start_row][start_col] == 'T':
        return True

    return dfs(grid, start_row + 1, start_col, end_row, end_col, visited) or \
           dfs(grid, start_row - 1, start_col, end_row, end_col, visited) or \
           dfs(grid, start_row, start_col + 1, end_row, end_col, visited) or \
           dfs(grid, start_row, start_col - 1, end_row, end_col, visited)

def generate_grid(n, start_row, start_col, end_row, end_col):
    grid = [['.' for _ in range(n)] for _ in range(n)]
    grid[start_row][start_col] = 'S'
    grid[end_row][end_col] = 'T'
    path = []
    current_row, current_col = start_row, start_col
    while current_row != end_row or current_col != end_col:
        if current_row < end_row:
            current_row += 1
        elif current_row > end_row:
            current_row -= 1
        if current_col < end_col:
            current_col += 1
        elif current_col > end_col:
            current_col -= 1
        path.append((current_row, current_col))

    wall_count = 0
    while wall_count < n * n // 4:
        row = random.randint(0, n - 1)
        col = random.randint(0, n - 1)
        if (row, col) not in path and (row, col) != (start_row, start_col) and (row, col) != (end_row, end_col):
            grid[row][col] = '#'
            wall_count += 1

    dfs(grid, start_row, start_col, end_row, end_col, set())
    return grid

n = int(input("Enter the grid size: "))
grid = generate_grid(n, 0, 0, n - 1, n - 1)
dist = [[None for _ in range(n)] for _ in range(n)]
parent = [[None for _ in range(n)] for _ in range(n)]
for line in grid:
    print(''.join(line))
start_row, start_col = None, None
end_row, end_col = None, None

for row in range(n):
    for col in range(n):
        if grid[row][col] == 'S':
            start_row, start_col = row, col
        elif grid[row][col] == 'T':
            end_row, end_col = row, col
    
def bfs():
    Q = deque()
    Q.append((start_row, start_col))
    dist[start_row][start_col] = 0
    while len(Q) > 0:
        row, col = Q.popleft()
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r = (row + dr) % n
            c = (col + dc) % n
            if grid[r][c] != '#' and dist[r][c] is None:
                dist[r][c] = dist[row][col] + 1
                parent[r][c] = (row, col)
                Q.append((r, c))


bfs()
print(n)

route = []
end_row, end_col = parent[end_row][end_col]
while parent[end_row][end_col] is not None:
    route.append((end_row, end_col))
    end_row, end_col = parent[end_row][end_col]

for step, (row, col) in enumerate(route[::-1], start=1):
    output = deepcopy(grid)
    for r, c in route[::-1][:step]:
        output[r][c] = 'O'
for line in output:
    print(''.join(line))
    time.sleep(0.1)     # Delay of 10ms
