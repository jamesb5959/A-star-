import time

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, cost=0):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = cost

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Initialize number of nodes created
    num_nodes = 0

    # Start time
    start_time = time.time()

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            end_time = time.time()
            runtime = (end_time - start_time) * 1000  # in milliseconds
            return path[::-1], num_nodes, runtime # Return reversed path, num_nodes, and runtime

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Four possible moves: Up, Down, Left, Right
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 0: # Impassable terrain
                continue

            # Create new node
            new_cost = maze[node_position[0]][node_position[1]] # Cost for moving to this position
            new_node = Node(current_node, node_position, new_cost)
            num_nodes += 1

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + child.cost
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1]) # Manhattan distance heuristic
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

    # If no path found
    end_time = time.time()
    runtime = (end_time - start_time) * 1000  # in milliseconds
    return [], num_nodes, runtime

def main():
    maze = [[1, 3, 2, 5, 1, 4, 3],
            [2, 1, 3, 1, 3, 2, 5],
            [3, 0, 5, 0, 1, 2, 2],
            [5, 3, 2, 1, 5, 0, 3],
            [2, 4, 1, 0, 0, 2, 0],
            [4, 0, 2, 1, 5, 3, 4],
            [1, 5, 1, 0, 2, 4, 1]]
           # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
           # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (3, 6)
    end = (5, 1)

    path, num_nodes, runtime = astar(maze, start, end)

    if path:
        print("1) The cost of the path found:", sum(maze[node[0]][node[1]] for node in path))
        print("2) The path as a sequence of coordinates:", path)
    else:
        print("1) The cost of the path found:", -1)
        print("2) The path sequence:", "NULL")

    print("3) The number of nodes created:", num_nodes)
    print("4) The runtime of the algorithm in milliseconds:", runtime)

if __name__ == '__main__':
    main()
