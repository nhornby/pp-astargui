# astar.py

# Function called "astar_search" that takes in:
# A matrix of 0s and 1s
# Two (x, y) coordinates representing the start and end
# Returns a list of (x, y) coordinates representing the
#       path from (inclusive) start to end

# Author: Nolan Hornby
# Date: September 7th, 2020
# University of Michigan
# Class of 2023

# Credit: This algorithm makes use of Patrick Lester's pseudocode for an A* algorithm, but is written by me.


class Node:
    def __init__(self, pos_in, parent_in):
        self.pos = pos_in
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = parent_in

    # Defines less than as being of lesser f-cost
    def __lt__(self, other):
        return self.f < other.f

    # Defines equality as being at the same position
    def __eq__(self, other):
        return self.pos == other.pos


def astar_search(matrix, start, end):
    if matrix[start[0]][start[1]] == 1:
        return []

    start_node = Node(start, None)
    end_node = Node(end, None)

    open_list = [start_node]
    closed_list = []

    while len(open_list) > 0:
        # Set current to lowest F in open_list, switch it closed_list
        open_list.sort()
        current = open_list.pop(0)
        closed_list.append(current)

        # Create a list all nearby spaces, given that they're not walls or out of bounds
        children = []
        for rr in [-1, 0, 1]:
            for cc in [-1, 0, 1]:
                if rr == 0 and cc == 0:
                    continue
                coord = (current.pos[0] + rr, current.pos[1] + cc)
                if (0 <= coord[0] < len(matrix)) and (0 <= coord[1] < len(matrix)) and matrix[coord[0]][coord[1]] == 0:
                    children.append(Node(coord, current))

        # For all of these children
        for child in children:
            # If you're at the end, return the path there
            if child == end_node:
                path = []
                while child != start_node:
                    path.append(child.pos)
                    child = child.parent
                path.append(start)
                return path

            # If it's in the closed list, skip it
            if child in closed_list:
                continue

            # Heuristic calculations
            child.g = current.g + 1
            if ((child.pos[0] - current.pos[0]) + (child.pos[1] - current.pos[1])) % 2 == 0:
                child.g += 0.4
            child.h = abs(child.pos[0] - end_node.pos[0]) + abs(child.pos[1] - end_node.pos[1])
            child.f = child.g + child.h

            # Add it to open if it's not looked at yet, or if we found a better path here.
            skip = False
            for open_node in open_list:
                if child == open_node and child.f >= open_node.f:
                    skip = True
            if not skip:
                open_list.append(child)
    return []
