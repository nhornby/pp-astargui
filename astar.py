# astar.py
import math

# Function called "astar" that takes in:
# A matrix of 0s and 1s
# Two (x, y) coordinates representing the start and end
# Returns a list of (x, y) coordinates representing the
#       path from (inclusive) start to end

# Author: Nolan Hornby
# Date: September 25th, 2020
# University of Michigan
# Class of 2023

DIAGONAL = True  # Can you move diagonally?

# --------------------------------------- DO NOT MODIFY BELOW THIS LINE -------------------------------------------

def astar(map, start, goal):

    # If the start or end is blocked, return nothing
    if map[start[0]][start[1]] == 1 or map[goal[0]][goal[1]] == 1:
        return ([], [])

    # Start and goal nodes
    start_node = Node(start, None)
    goal_node = Node(goal, None)

    # Open and closed lists
    open_list = [start_node]
    closed_list = []

    # Main A* loop
    while len(open_list) > 0:

        # Choose lowest-cost node from open_list and remove it
        open_list.sort()
        current_node = open_list.pop(0)
        closed_list.append(current_node)

        # Get any valid children from this node
        children = []
        for rr in [-1, 0, 1]:
            for cc in [-1, 0, 1]:
                coord = (current_node.pos[0] + rr, current_node.pos[1] + cc)
                if rr == 0 and cc == 0:
                    continue
                if coord[0] < 0 or coord[1] < 0 or coord[0] >= len(map) or coord[1] >= len(map):
                    continue
                if map[coord[0]][coord[1]] == 1:
                    continue
                if rr != 0 and cc != 0:
                    if not DIAGONAL:
                        continue
                    if map[coord[0]][coord[1] - cc] == 1 and map[coord[0] - rr][coord[1]] == 1:
                        continue
                children.append(Node(coord, current_node))

        # For each child
        for child in children:
            # If the end has been reached, return the path there and the closed_list
            if child == goal_node:
                path = []
                while child != start_node:
                    path.append(child.pos)
                    child = child.parent
                path.append(start_node.pos)
                return (path, get_coords(closed_list))

            # If this node has already been examined, skip it
            if child in closed_list:
                continue

            # Do heuristic calculations for this child
            child.g = current_node.g + 1
            if ((child.pos[0] - current_node.pos[0]) + (child.pos[1] - current_node.pos[1])) % 2 == 0:
                child.g += 0.4
            child.h = abs(child.pos[0] - goal_node.pos[0]) + abs(child.pos[1] - goal_node.pos[1])
            child.f = child.g + child.h

            # Make sure that we don't already have a better path to this node before adding it to open_list
            if all((child.f < open_node.f) or (child != open_node) for open_node in open_list):
                open_list.append(child)

    # If you get nowhere, there is no path to the finish.
    return ([], get_coords(closed_list))

# Takes in a list of Nodes, returns a list of coordinates.
def get_coords(nodes):
    coord_list = []
    for node in nodes:
        coord_list.append(node.pos)
    return coord_list


# Node class
class Node:
    def __init__(self, pos_in, parent_in):
        self.pos = pos_in
        self.f = 0.0
        self.g = 0.0
        self.h = 0.0
        self.parent = parent_in

    # Defines less than as being of lesser f-cost
    def __lt__(self, other):
        return self.f < other.f

    # Defines equality as being at the same position
    def __eq__(self, other):
        return self.pos == other.pos
