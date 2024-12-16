import pygame
import time
import math
import heapq
import random

GRID_SIZE = 10
CELL_SIZE = 70
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FEEDBACK_HEIGHT = 50
WINDOW_HEIGHT = WINDOW_SIZE + FEEDBACK_HEIGHT
STEP_DELAY = 0.3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))
pygame.display.set_caption("Robot Navigation with Obstacles")
font = pygame.font.Font(None, 36)

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pygame.draw.rect(window, WHITE, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, BLACK, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def calculate_center(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    center_x = sum(x_coords) // len(points)
    center_y = sum(y_coords) // len(points)
    return center_x, center_y

def draw_feedback(feedback):
    pygame.draw.rect(window, GRAY, (0, WINDOW_SIZE, WINDOW_SIZE, FEEDBACK_HEIGHT))
    feedback_text = font.render(feedback, True, BLACK)
    window.blit(feedback_text, (10, WINDOW_SIZE + 2))
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

def get_starting_position():
    x, y = pygame.mouse.get_pos()
    return (y // CELL_SIZE, x // CELL_SIZE)

def main():
    running = True
    points = []
    robot_position = None
    path = []
    center = None
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    feedback = "Click to define the four corners of the rectangle."
    placing_obstacles = False
    specified_start = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE

                if len(points) < 4:
                    if (x, y) not in points:  
                        points.append((x, y))
                        feedback = f"Point {len(points)} selected at {x, y}."
                        grid[x][y] = 1

                elif placing_obstacles:
                    if (x, y) not in points and (x, y) != center:  
                        if grid[x][y] == 0:  
                            grid[x][y] = 1
                            feedback = f"Obstacle placed at {x, y}."
                        elif grid[x][y] == 1:  
                            grid[x][y] = 0
                            feedback = f"Obstacle removed at {x, y}."

                elif specified_start is None:
                    specified_start = get_starting_position()
                    feedback = f"Starting position set at {specified_start}. Press SPACE to calculate path."

                if len(points) == 4 and not placing_obstacles:
                    center = calculate_center(points)
                    feedback = f"Center calculated at {center}. Press SPACE to start or 'O' to place obstacles."

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(points) == 4 and specified_start:
                    robot_position = specified_start
                    path = a_star(grid, robot_position, center)
                    feedback = f"Path calculated to center at {center}."
                elif event.key == pygame.K_o and len(points) == 4:
                    placing_obstacles = not placing_obstacles
                    feedback = "Click to place/remove obstacles. Press 'O' again to finish."

        window.fill(WHITE)
        draw_grid()

        
        for point in points:
            pygame.draw.circle(window, RED, (point[1] * CELL_SIZE + CELL_SIZE // 2, point[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

       
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if grid[x][y] == 1 and (x, y) not in points:
                    pygame.draw.rect(window, BLUE, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        
        if robot_position and path:
            next_step = path.pop(0)
            pygame.draw.rect(window, YELLOW, (next_step[1] * CELL_SIZE, next_step[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            robot_position = next_step
            feedback = f"Robot moved to {robot_position}."
            if not path:
                feedback = "Robot reached the center!"

        
        if robot_position:
            pygame.draw.circle(window, GREEN, (robot_position[1] * CELL_SIZE + CELL_SIZE // 2, robot_position[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

        draw_feedback(feedback)
        pygame.display.update()
        time.sleep(STEP_DELAY)

main()
pygame.quit()
