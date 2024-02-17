#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#define MAZE_WIDTH 10
#define MAZE_HEIGHT 10

typedef struct Node {
    struct Node *parent;
    int position[2];
    int g, h, f;
} Node;

Node* createNode(Node* parent, int x, int y) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->parent = parent;
    node->position[0] = x;
    node->position[1] = y;
    node->g = 0;
    node->h = 0;
    node->f = 0;
    return node;
}

bool isEqual(Node* node1, Node* node2) {
    return (node1->position[0] == node2->position[0]) && (node1->position[1] == node2->position[1]);
}

Node* findPath(int maze[MAZE_HEIGHT][MAZE_WIDTH], int start[2], int end[2]) {
    Node* startNode = createNode(NULL, start[0], start[1]);
    startNode->g = startNode->h = startNode->f = 0;
    Node* endNode = createNode(NULL, end[0], end[1]);
    endNode->g = endNode->h = endNode->f = 0;

    Node* openList[MAZE_WIDTH * MAZE_HEIGHT];
    Node* closedList[MAZE_WIDTH * MAZE_HEIGHT];
    int openListSize = 0;

    openList[openListSize++] = startNode;

    while (openListSize > 0) {
        Node* currentNode = openList[0];
        int currentIndex = 0;
        for (int i = 0; i < openListSize; i++) {
            if (openList[i]->f < currentNode->f) {
                currentNode = openList[i];
                currentIndex = i;
            }
        }

        // Pop current off open list, add to closed list
        for (int i = currentIndex; i < openListSize - 1; i++) {
            openList[i] = openList[i + 1];
        }
        openListSize--;
        closedList[currentIndex] = currentNode;

        if (isEqual(currentNode, endNode)) {
            Node* current = currentNode;
            while (current != NULL) {
                printf("(%d, %d)\n", current->position[0], current->position[1]);
                current = current->parent;
            }
            return currentNode; // Return end node
        }

        // Generate children
        Node* children[8];
        int directions[8][2] = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}}; // Adjacent squares

        for (int i = 0; i < 8; i++) {
            int newX = currentNode->position[0] + directions[i][0];
            int newY = currentNode->position[1] + directions[i][1];

            // Make sure within range
            if (newX >= 0 && newX < MAZE_HEIGHT && newY >= 0 && newY < MAZE_WIDTH) {
                // Make sure walkable terrain
                if (maze[newX][newY] == 0) {
                    Node* newNode = createNode(currentNode, newX, newY);
                    children[i] = newNode;
                } else {
                    children[i] = NULL;
                }
            } else {
                children[i] = NULL;
            }
        }

        // Loop through children
        for (int i = 0; i < 8; i++) {
            Node* child = children[i];
            if (child == NULL) continue;

            // Child is on the closed list
            bool foundInClosed = false;
            for (int j = 0; j < openListSize; j++) {
                if (isEqual(child, closedList[j])) {
                    foundInClosed = true;
                    break;
                }
            }
            if (foundInClosed) continue;

            // Create the f, g, and h values
            child->g = currentNode->g + 1;
            child->h = pow((child->position[0] - endNode->position[0]), 2) + pow((child->position[1] - endNode->position[1]), 2);
            child->f = child->g + child->h;

            // Child is already in the open list
            bool foundInOpen = false;
            for (int j = 0; j < openListSize; j++) {
                if (isEqual(child, openList[j]) && child->g > openList[j]->g) {
                    foundInOpen = true;
                    break;
                }
            }
            if (foundInOpen) continue;

            // Add the child to the open list
            openList[openListSize++] = child;
        }
    }
    return NULL; // No path found
}

int main() {
    int maze[MAZE_HEIGHT][MAZE_WIDTH] = {
        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
    };

    int start[2] = {0, 0};
    int end[2] = {7, 6};

    Node* path = findPath(maze, start, end);
    if (path == NULL) {
        printf("No path found.\n");
    }

    return 0;
}
