
#2:There are up to 3 gems in the grid, denoted as ‘G’. Before we get to the target, we need to collect them in any order. It is possible that the total path will visit the same cell multiple times.

import random
from collections import deque
from copy import deepcopy

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

    gem_count = 0
    while gem_count < 3:
        row = random.randint(0, n - 1)
        col = random.randint(0, n - 1)
        if grid[row][col] == '.' and (row, col) not in path and (row, col) != (start_row, start_col) and (row, col) != (end_row, end_col):
            grid[row][col] = 'G'
            gem_count += 1

    return grid

def dfs(grid, start_row, start_col, end_row, end_col, visited, gems):
    if start_row < 0 or start_row >= len(grid) or start_col < 0 or start_col >= len(grid[0]) or grid[start_row][start_col] == '#' or (start_row, start_col) in visited:
        return False

    visited.add((start_row, start_col))

    if grid[start_row][start_col] == 'G':
        gems.remove((start_row, start_col))

    if len(gems) == 0 and grid[start_row][start_col] == 'T':
        return True

    result = dfs(grid, start_row + 1, start_col, end_row, end_col, visited, gems) or \
             dfs(grid, start_row - 1, start_col, end_row, end_col, visited, gems) or \
             dfs(grid, start_row, start_col + 1, end_row, end_col, visited, gems) or \
             dfs(grid, start_row, start_col - 1, end_row, end_col, visited, gems)

    if not result:
        if grid[start_row][start_col] == 'G':
            gems.add((start_row, start_col))

    return result



n = int(input("Enter the grid size: "))
grid = generate_grid(n, 0, 0, n - 1, n - 1)

dist = [[None for _ in range(n)] for _ in range(n)]
parent = [[None for _ in range(n)] for _ in range(n)]
start_row, start_col = None, None
end_row, end_col = None, None
gems = set()

for row in range(n):
    for col in range(n):
        if grid[row][col] == 'S':
            start_row, start_col = row, col
        elif grid[row][col] == 'T':
            end_row, end_col = row, col
        elif grid[row][col] == 'G':
            gems.add((row, col))

def bfs():
    Q = deque()
    Q.append((start_row, start_col))
    dist[start_row][start_col] = 0
    while len(Q) > 0:
        row, col = Q.popleft()
        for r, c in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
            if 0 <= r < n and 0 <= c < n and grid[r][c] != '#' and dist[r][c] is None:
                dist[r][c] = dist[row][col] + 1
                parent[r][c] = (row, col)
                Q.append((r, c))
                if (r, c) in gems:
                    gems.remove((r, c))
                if len(gems) == 0 and (r, c) == (end_row, end_col):
                    return

bfs()

route = []
end_row, end_col = parent[end_row][end_col]
while parent[end_row][end_col] is not None:
    route.append((end_row, end_col))
    end_row, end_col = parent[end_row][end_col]

output = deepcopy(grid)
for row, col in route[::-1]:
    output[row][col] = 'O'

for line in output:
    print(''.join(line))
