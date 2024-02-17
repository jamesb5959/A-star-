import java.util.ArrayList;
import java.util.List;

class Node {
    // A node class for A* Pathfinding

    Node parent;
    int[] position;
    int g, h, f;

    public Node(Node parent, int[] position) {
        this.parent = parent;
        this.position = position;
        this.g = 0;
        this.h = 0;
        this.f = 0;
    }

    public boolean equals(Node other) {
        return this.position[0] == other.position[0] && this.position[1] == other.position[1];
    }
}

public class AStar {

    public static List<int[]> astar(int[][] maze, int[] start, int[] end) {
        // Returns a list of arrays as a path from the given start to the given end in the given maze

        // Create start and end node
        Node startNode = new Node(null, start);
        startNode.g = startNode.h = startNode.f = 0;
        Node endNode = new Node(null, end);
        endNode.g = endNode.h = endNode.f = 0;

        // Initialize both open and closed list
        List<Node> openList = new ArrayList<>();
        List<Node> closedList = new ArrayList<>();

        // Add the start node
        openList.add(startNode);

        // Loop until you find the end
        while (!openList.isEmpty()) {

            // Get the current node
            Node currentNode = openList.get(0);
            int currentIndex = 0;
            for (int i = 0; i < openList.size(); i++) {
                if (openList.get(i).f < currentNode.f) {
                    currentNode = openList.get(i);
                    currentIndex = i;
                }
            }

            // Pop current off open list, add to closed list
            openList.remove(currentIndex);
            closedList.add(currentNode);

            // Found the goal
            if (currentNode.equals(endNode)) {
                List<int[]> path = new ArrayList<>();
                Node current = currentNode;
                while (current != null) {
                    path.add(current.position);
                    current = current.parent;
                }
                List<int[]> reversedPath = new ArrayList<>();
                for (int i = path.size() - 1; i >= 0; i--) {
                    reversedPath.add(path.get(i));
                }
                return reversedPath; // Return reversed path
            }

            // Generate children
            List<Node> children = new ArrayList<>();
            int[][] directions = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}}; // Adjacent squares

            for (int[] direction : directions) {
                int[] newPosition = {currentNode.position[0] + direction[0], currentNode.position[1] + direction[1]};

                // Make sure within range
                if (newPosition[0] > maze.length - 1 || newPosition[0] < 0 || newPosition[1] > maze[0].length - 1 || newPosition[1] < 0) {
                    continue;
                }

                // Make sure walkable terrain
                if (maze[newPosition[0]][newPosition[1]] != 0) {
                    continue;
                }

                // Create new node
                Node newNode = new Node(currentNode, newPosition);

                // Append
                children.add(newNode);
            }

            // Loop through children
            for (Node child : children) {

                // Child is on the closed list
                boolean foundInClosed = false;
                for (Node closedChild : closedList) {
                    if (child.equals(closedChild)) {
                        foundInClosed = true;
                        break;
                    }
                }
                if (foundInClosed) {
                    continue;
                }

                // Create the f, g, and h values
                child.g = currentNode.g + 1;
                child.h = (int) (Math.pow((child.position[0] - endNode.position[0]), 2) + Math.pow((child.position[1] - endNode.position[1]), 2));
                child.f = child.g + child.h;

                // Child is already in the open list
                boolean foundInOpen = false;
                for (Node openNode : openList) {
                    if (child.equals(openNode) && child.g > openNode.g) {
                        foundInOpen = true;
                        break;
                    }
                }
                if (foundInOpen) {
                    continue;
                }

                // Add the child to the open list
                openList.add(child);
            }
        }
        return null; // No path found
    }

    public static void main(String[] args) {
        int[][] maze = {{0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
                        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}};

        int[] start = {0, 0};
        int[] end = {7, 6};

        List<int[]> path = astar(maze, start, end);
        if (path != null) {
            for (int[] position : path) {
                System.out.println("(" + position[0] + ", " + position[1] + ")");
            }
        } else {
            System.out.println("No path found.");
        }
    }
}
