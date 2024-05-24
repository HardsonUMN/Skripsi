import heapq
import numpy as np
import matplotlib.pyplot as plt
import time

# Define the size of the grid
GRID_SIZE = 20
OBSTACLE = 1
FREE_SPACE = 0

# Initialize the grid
grid = np.zeros((GRID_SIZE, GRID_SIZE))
# Example obstacles (this should be updated with actual sensor data)
grid[5, 5:10] = OBSTACLE
grid[10, 10:15] = OBSTACLE
grid[15, 2:20] = OBSTACLE
# Heuristic function for A* (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* pathfinding algorithm
def astar(grid, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1

            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if grid[neighbor[0]][neighbor[1]] == OBSTACLE:
                    continue
            else:
                # grid boundary
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

def plot_grid(grid, path=None, robot_pos=None):
    plt.clf()
    plt.imshow(grid, cmap='gray_r', origin='upper')
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, 'b', label='Path')
    if robot_pos:
        plt.plot(robot_pos[1], robot_pos[0], 'go', label='Robot')
    plt.xlim(-0.5, GRID_SIZE - 0.5)
    plt.ylim(-0.5, GRID_SIZE - 0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.grid(True)
    plt.pause(0.01)  # Pause to allow the plot to update

# Main loop for path planning and visualization
def main():
    global grid

    start = (0, 0)
    goal = (19, 19)

    plt.ion()  # Turn on interactive mode

    while True:
        path = astar(grid, start, goal)
        
        if path:
            path = path[::-1]  # reverse path
            print("Path found:")
            for step in path:
                print(step)
        else:
            print("No path found")
        
        plot_grid(grid, path, start)  # Pass the robot's initial position

        # Simulate robot movement along the path
        if path:
            for step in path:
                start = step
                print(f"Robot moves to: {start}")
                plot_grid(grid, path, start)  # Pass the robot's position
                time.sleep(1)

        if start == goal:
            print("Goal reached!")
            break

# Run the main loop
if __name__ == "__main__":
    main()
