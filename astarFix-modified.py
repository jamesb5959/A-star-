import random
import sys
from warnings import warn
import heapq
import time

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None, cost=0):
        self.parent = parent
        self.position = position
        self.cost = cost

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, heuristic = 2, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    totalNodes = 0
    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        # if outer_iterations > max_iterations:
        #   # if we hit this point return the path such as it is
        #   # it will not contain the destination
        #   warn("giving up on pathfinding too many iterations")
        #   return (return_path(current_node), totalNodes)

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return (return_path(current_node), totalNodes)

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 0:
                continue

            # Create new node
            totalNodes += 1
            nodeCost = maze[node_position[0]][node_position[1]]
            new_node = Node(current_node, node_position, nodeCost)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + child.cost

            match heuristic:
                case 1:
                    child.h = 0
                case 2:
                    child.h = manhattanHeuristic(child, end_node)
                case 3:
                    child.h = modManhattanHeuristic(child, end_node)
                case 4:
                    child.h = errorManhattanHeuristic(child, end_node)
                case _:
                    child.h = manhattanHeuristic(child, end_node)

            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return ([], totalNodes)

#def zeroHeuristic(node, end_node):
#   """Heuristic H1: All zeros"""
#  return 0

def manhattanHeuristic(node, endNode):
    return abs(node.position[0] - endNode.position[0]) + abs(node.position[1] - endNode.position[1])

def modManhattanHeuristic(node, endNode):
    # This heuristic is still admissible but more accurate; it could be, for example, Manhattan distance multiplied by a constant factor
    #return 2 * (abs(node.position[0] - end_node.position[0]) + abs(node.position[1] - end_node.position[1]))
    # multiplies the original sum from the manhattanHeuristic by half the cost of the node
    return (0.5 * node.cost) * abs(node.position[0] - endNode.position[0]) + abs(node.position[1] - endNode.position[1])

#def errorManhattanHeuristic(node, endnode):
#    """Heuristic H4: Manhattan distance with error"""
#    # Add errors from -10 to +10, excluding 0 with a uniform random distribution
#    error = random.randint(-10, 10)
#    if error == 0:
#        error = 1 if random.random() < 0.5 else -1
#    return max(0, abs(node.position[0] - endnode.position[0]) + abs(node.position[1] - endnode.position[1]) + error)

def errorManhattanHeuristic(node, endNode):
    # Standard Manhattan distance calculation
    manhattanDistance = manhattanHeuristic(node, endNode)
    # Generate a random error between -10 and 10, excluding 0
    error = random.choice(list(range(-10, 0)) + list(range(1, 11)))
    # Add the error to the Manhattan distance
    adjustedDistance = manhattanDistance + error
    # Ensure the heuristic is at least 0
    if adjustedDistance < 0:
        adjustedDistance = 0
    return adjustedDistance

def termMain(testCase = 1, heuristic = 2):
    if not (heuristic >= 1 and heuristic <= 4):
        heuristic = 2
    match testCase:
        case '1':
            maze = [
                [2, 4, 2, 1, 4, 5, 2],
                [0, 1, 2, 3, 5, 3, 1],
                [2, 0, 4, 4, 1, 2, 4],
                [2, 5, 5, 3, 2, 0, 1],
                [4, 3, 3, 2, 1, 0, 1]
            ]
            start = (1, 2)
            end = (4, 3)
        case '2':
            maze = [
                [1, 3, 2, 5, 1, 4, 3],
                [2, 1, 3, 1, 3, 2, 5],
                [3, 0, 5, 0, 1, 2, 2],
                [5, 3, 2, 1, 5, 0, 3],
                [2, 4, 1, 0, 0, 2, 0],
                [4, 0, 2, 1, 5, 3, 4],
                [1, 5, 1, 0, 2, 4, 1]
            ]
            start = (3, 6)
            end = (5, 1)
        case '3':
            maze = [
                [2, 0, 2, 0, 2, 0, 0, 2, 2, 0],
                [1, 2, 3, 5, 2, 1, 2, 5, 1, 2],
                [2, 0, 2, 2, 1, 2, 1, 2, 4, 2],
                [2, 0, 1, 0, 1, 1, 1, 0, 0, 1],
                [1, 1, 0, 0, 5, 0, 3, 2, 2, 2],
                [2, 2, 2, 2, 1, 0, 1, 2, 1, 0],
                [1, 0, 2, 1, 3, 1, 4, 3, 0, 1],
                [2, 0, 5, 1, 5, 2, 1, 2, 4, 1],
                [1, 2, 2, 2, 0, 2, 0, 1, 1, 0],
                [5, 1, 2, 1, 1, 1, 2, 0, 1, 2]
            ]
            start = (1, 2)
            end = (8, 8)
        case '4':
            maze = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
            start = (0, 0)
            end = (4, 4)
        case '5':
            maze = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            ]
            start = (0, 0)
            end = (8, 8)
        case _: #default
            maze = [
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
            start = (0, 0)
            end = (7, 6)
    
    startTime = time.time()
    (path, totalNodes) = astar(maze, start, end, heuristic)
    endTime = time.time()
    if not path:
        cost = -1
        path = 'NULL'
    else:
        cost = 0
        for node in path:
            cost += maze[node[0]][node[1]]
    print(f'Maze:\n{maze}')
    print(f'Start:\n{start}')
    print(f'End:\n{end}')
    print(f'Heuristic:\n{heuristic}')
    print(f'Cost of path:\n{cost}')
    print(f'Path found:\n{path}')
    print(f'Nodes created:\n{totalNodes}')
    print(f'Execution time:\n{endTime - startTime}')
    print()


def main():    
    maze = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    end = (7, 6)
    print(f'{1}')
    for i in range(4):
        heuristicNum = i + 1
        print(f'Heuristic Number:\n{heuristicNum}')
        startTime = time.time()
        (path, totalNodes) = astar(maze, start, end, heuristicNum)
        endTime = time.time()
        if not path:
            cost = -1
            path = 'NULL'
        else:
            cost = 0
            for node in path:
                cost += maze[node[0]][node[1]]
        print(f'Cost of path:\n{cost}')
        print(f'Path found:\n{path}')
        print(f'Nodes created:\n{totalNodes}')
        print(f'Execution time:\n{endTime - startTime}')
        print()

    maze = [
        [2, 4, 2, 1, 4, 5, 2],
        [0, 1, 2, 3, 5, 3, 1],
        [2, 0, 4, 4, 1, 2, 4],
        [2, 5, 5, 3, 2, 0, 1],
        [4, 3, 3, 2, 1, 0, 1]
    ]
    start = (1, 2)
    end = (4, 3)
    print(f'{2}')
    for i in range(4):
        heuristicNum = i + 1
        print(f'Heuristic Number:\n{heuristicNum}')
        startTime = time.time()
        (path, totalNodes) = astar(maze, start, end, heuristicNum)
        endTime = time.time()
        if not path:
            cost = -1
            path = 'NULL'
        else:
            cost = 0
            for node in path:
                cost += maze[node[0]][node[1]]
        print(f'Cost of path:\n{cost}')
        print(f'Path found:\n{path}')
        print(f'Nodes created:\n{totalNodes}')
        print(f'Execution time:\n{endTime - startTime}')
        print()

    maze = [
        [1, 3, 2, 5, 1, 4, 3],
        [2, 1, 3, 1, 3, 2, 5],
        [3, 0, 5, 0, 1, 2, 2],
        [5, 3, 2, 1, 5, 0, 3],
        [2, 4, 1, 0, 0, 2, 0],
        [4, 0, 2, 1, 5, 3, 4],
        [1, 5, 1, 0, 2, 4, 1]
    ]
    start = (3, 6)
    end = (5, 1)
    print(f'{3}')
    for i in range(4):
        heuristicNum = i + 1
        print(f'Heuristic Number:\n{heuristicNum}')
        startTime = time.time()
        (path, totalNodes) = astar(maze, start, end, heuristicNum)
        endTime = time.time()
        if not path:
            cost = -1
            path = 'NULL'
        else:
            cost = 0
            for node in path:
                cost += maze[node[0]][node[1]]
        print(f'Cost of path:\n{cost}')
        print(f'Path found:\n{path}')
        print(f'Nodes created:\n{totalNodes}')
        print(f'Execution time:\n{endTime - startTime}')
        print()

    maze = [
        [2, 0, 2, 0, 2, 0, 0, 2, 2, 0],
        [1, 2, 3, 5, 2, 1, 2, 5, 1, 2],
        [2, 0, 2, 2, 1, 2, 1, 2, 4, 2],
        [2, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 0, 0, 5, 0, 3, 2, 2, 2],
        [2, 2, 2, 2, 1, 0, 1, 2, 1, 0],
        [1, 0, 2, 1, 3, 1, 4, 3, 0, 1],
        [2, 0, 5, 1, 5, 2, 1, 2, 4, 1],
        [1, 2, 2, 2, 0, 2, 0, 1, 1, 0],
        [5, 1, 2, 1, 1, 1, 2, 0, 1, 2]
    ]
    start = (1, 2)
    end = (8, 8)
    print(f'{4}')
    for i in range(4):
        heuristicNum = i + 1
        print(f'Heuristic Number:\n{heuristicNum}')
        startTime = time.time()
        (path, totalNodes) = astar(maze, start, end, heuristicNum)
        endTime = time.time()
        if not path:
            cost = -1
            path = 'NULL'
        else:
            cost = 0
            for node in path:
                cost += maze[node[0]][node[1]]
        print(f'Cost of path:\n{cost}')
        print(f'Path found:\n{path}')
        print(f'Nodes created:\n{totalNodes}')
        print(f'Execution time:\n{endTime - startTime}')
        print()

    # my test
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    start = (0, 0)
    end = (4, 4)
    print(f'{5}')
    for i in range(4):
        heuristicNum = i + 1
        print(f'Heuristic Number:\n{heuristicNum}')
        startTime = time.time()
        (path, totalNodes) = astar(maze, start, end, heuristicNum)
        endTime = time.time()
        if not path:
            cost = -1
            path = 'NULL'
        else:
            cost = 0
            for node in path:
                cost += maze[node[0]][node[1]]
        print(f'Cost of path:\n{cost}')
        print(f'Path found:\n{path}')
        print(f'Nodes created:\n{totalNodes}')
        print(f'Execution time:\n{endTime - startTime}')
        print()

    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]
    start = (0, 0)
    end = (8, 8)
    print(f'{6}')
    for i in range(4):
        heuristicNum = i + 1
        print(f'Heuristic Number:\n{heuristicNum}')
        startTime = time.time()
        (path, totalNodes) = astar(maze, start, end, heuristicNum)
        endTime = time.time()
        if not path:
            cost = -1
            path = 'NULL'
        else:
            cost = 0
            for node in path:
                cost += maze[node[0]][node[1]]
        print(f'Cost of path:\n{cost}')
        print(f'Path found:\n{path}')
        print(f'Nodes created:\n{totalNodes}')
        print(f'Execution time:\n{endTime - startTime}')
        print()

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print(f'NO ARGUMENTS WERE GIVEN')
    elif len(args) != 2:
        print(f'INVALID ARGUMENTS WERE GIVEN (RECEIVED {len(args)} ARGUMENTS, BUT TAKES 2 ARGUMENTS)')
    elif int(args[0]) <= 5 and int(args[1]) <= 4:
        termMain(args[0], int(args[1]))
    else:
        print(f'ARGUMENT 1 NEEDS TO BE <= 5 AND ARGUMENT 2 NEEDS TO BE <= 4')
