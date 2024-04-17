#Instead of printing ‘o’ for path cells, print the direction of next step, one of: <>v^. 
#Add visualization in any programming language. Display a grid with colored cells (or small icons).
#In the output, show the path growing step by step from the start to the target. That is, after every step: display the grid and sleep for 10ms (for better effect).
#Test your program by creating a function to generate input grids of different sizes. You can generate grids randomly or you can implement 2-3 predermined patterns (must work for various sizes of N). Make sure that there is a path between start and target.

#1,3,5,8
from collections import deque
from copy import deepcopy
import time
import random



#dfs to check  for available path for generation of grid
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

#add vizualization for coloring the grid
def draw_grid(grid):
    WALL_COLOR = '\033[37;40m'
    START_COLOR = '\033[31;40m'
    END_COLOR = '\033[34;40m'
    EMPTY_COLOR = '\033[32;40m'
    PATH_COLOR = '\033[33;40m'
    RESET_COLOR = '\033[0m'
    for line in grid:
        colored_line = ''
        for cell in line:
            if cell == '#':
                colored_line += WALL_COLOR + '██' + RESET_COLOR
            elif cell == 'S':
                colored_line += START_COLOR + '██' + RESET_COLOR
            elif cell == 'T':
                colored_line += END_COLOR + '██' + RESET_COLOR
            elif cell == 'O':
                colored_line += PATH_COLOR + '██' + RESET_COLOR
            else:
                colored_line += EMPTY_COLOR + '░░' + RESET_COLOR
        print(colored_line)



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
        for r, c in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
            if 0 <= r < n and 0 <= c < n and grid[r][c]!= '#' and dist[r][c] is None:
                dist[r][c] = dist[row][col] + 1
                parent[r][c] = (row, col)
                Q.append((r, c))

bfs()
print()
print("output for  delayed effect")
print(n)
route = []
end_row, end_col = parent[end_row][end_col]
while parent[end_row][end_col] is not None:
    route.append((end_row, end_col))
    end_row, end_col = parent[end_row][end_col]
# output after generate Grid

output = deepcopy(grid)
for row, col in route[::-1]:
    output[row][col] = 'O'

for line in output:
    print(''.join(line))
    time.sleep(0.1) 

print()
print("Colored Grid")
draw_grid(output)
print()

#Instead of printing ‘o’ for path cells, print the direction of next step, one of: <>v^. 
print("Using directional arrows")
for i in range(len(route) - 1):
    curr_row, curr_col = route[i]
    next_row, next_col = route[i+1]
    if next_row > curr_row:
        output[curr_row][curr_col] = 'v'
    elif next_row < curr_row:
        output[curr_row][curr_col] = '^'
    elif next_col > curr_col:
        output[curr_row][curr_col] = '>'
    else:
        output[curr_row][curr_col] = '<'
for line in output:
    print(''.join(line))
