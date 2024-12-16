import pygame
import random
import time
import heapq


GRID_SIZE = 10
CELL_SIZE = 50
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FEEDBACK_HEIGHT = 50
WINDOW_HEIGHT = WINDOW_SIZE + FEEDBACK_HEIGHT
OBSTACLE_COUNT = 30
MOVE_INTERVAL = 3  
STEP_DELAY = 0.5   


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)


pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))
pygame.display.set_caption("Dynamic Robot Navigation")
font = pygame.font.Font(None, 36)


def initialize_grid(start, end):
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    obstacles = []
    while len(obstacles) < OBSTACLE_COUNT:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if grid[x][y] == 0 and (x, y) != start and (x, y) != end:  
            grid[x][y] = 1
            obstacles.append((x, y))
    return grid, obstacles


def draw_grid(grid, robot, end, path, obstacles, feedback):
    window.fill(WHITE)
    
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = WHITE if grid[x][y] == 0 else RED
            pygame.draw.rect(window, color, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, BLACK, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    
    
    pygame.draw.circle(window, GREEN, (robot[1]*CELL_SIZE+CELL_SIZE//2, robot[0]*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//4)
    
    pygame.draw.circle(window, BLUE, (end[1]*CELL_SIZE+CELL_SIZE//2, end[0]*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//4)
    
    
    for x, y in path:
        pygame.draw.rect(window, YELLOW, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    
    pygame.draw.rect(window, GRAY, (0, WINDOW_SIZE, WINDOW_SIZE, FEEDBACK_HEIGHT))
    feedback_text = font.render(feedback, True, BLACK)
    window.blit(feedback_text, (10, WINDOW_SIZE + 10))
    
    pygame.display.update()


def a_star(grid, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    while open_list:
        _, current = heapq.heappop(open_list)
        if current == end:
            return reconstruct_path(came_from, current)
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    return []


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def give_feedback(robot, next_step, grid):
    direction = ""
    if next_step[0] > robot[0]: direction = "down"
    elif next_step[0] < robot[0]: direction = "up"
    elif next_step[1] > robot[1]: direction = "right"
    elif next_step[1] < robot[1]: direction = "left"
    
    return f"Robot moved {direction} to {next_step}."


def main():
    start, end = (0, 0), (9, 9)
    grid, obstacles = initialize_grid(start, end)
    robot = start
    path = a_star(grid, start, end)
    last_move_time = time.time()
    feedback = "Click on the window to set start and end points."
    setting_start = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if setting_start:
                    start = (event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE)
                    grid, obstacles = initialize_grid(start, end)  # Reset grid with new start
                    robot = start
                    setting_start = False
                    feedback = "Click on the window to set the end point."
                else:
                    end = (event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE)
                    grid, obstacles = initialize_grid(start, end)  # Reset grid with new end
                    path = a_star(grid, start, end)
                    feedback = "Click on the window to move the robot."
        

        if time.time() - last_move_time > MOVE_INTERVAL:
            for i in range(len(obstacles)):
                x, y = obstacles[i]
                grid[x][y] = 0
                while True:
                    nx, ny = x + random.choice([-1, 0, 1]), y + random.choice([-1, 0, 1])
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] == 0 and (nx, ny) != start and (nx, ny) != end:
                        obstacles[i] = (nx, ny)
                        grid[nx][ny] = 1
                        break
            last_move_time = time.time()
            path = a_star(grid, robot, end)  

        
        if path:
            next_step = path.pop(0)
            feedback = give_feedback(robot, next_step, grid)
            robot = next_step
            if robot == end:
                feedback = "Robot reached the destination!"
                running = False
        
        draw_grid(grid, robot, end, path, obstacles, feedback)
        time.sleep(STEP_DELAY)

main()
pygame.quit()
