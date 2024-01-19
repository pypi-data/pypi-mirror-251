from __future__ import annotations
from enum import Enum
from collections import defaultdict
import random

class Direction(Enum):
    NORTH = 'north'
    SOUTH = 'south'
    WEST  = 'west'
    EAST  = 'east'

class Maze:
    opposite_of = {
        Direction.NORTH: Direction.SOUTH,
        Direction.SOUTH: Direction.NORTH,
        Direction.WEST:  Direction.EAST,
        Direction.EAST:  Direction.WEST
    }

    def __init__(self, height: int, width: int) -> None:
        if height < 3:
            raise Exception("ERROR: Invalid height, must be >= 3.")
        if width < 3:
            raise Exception("ERROR: Invalid width, must be >= 3.")

        self.height = height
        self.width = width
        self.maze = defaultdict(int)

    def make(self, x: int = 0, y: int = 0) -> Maze:
        directions = list(self.opposite_of.keys())
        random.shuffle(directions)
        for direction in directions:
            new_x, new_y = x, y
            if direction == Direction.EAST:
                new_x = new_x + 1
            elif direction == Direction.WEST:
                new_x = new_x - 1
            elif direction == Direction.SOUTH:
                new_y = new_y + 1
            else:
                new_y = new_y - 1

            if self.not_visited(new_x, new_y):
                self.update(x, y, direction)
                self.update(new_x, new_y, self.opposite_of[direction])
                self.make(new_x, new_y)

        return self

    def update(self, x: int, y: int, direction) -> None:
        if y in self.maze:
            if x in self.maze.get(y):
                item = self.maze.get(y).get(x)
                item[direction] = 1
                self.maze[y][x] = item
            else:
                self.maze[y][x] = { direction: 1 }
        else:
            self.maze[y] = { x: { direction: 1 } }

    def not_visited(self, x: int, y: int) -> bool:
        if (x < 0) or (y < 0):
            return False
        if (x > (self.width - 1)) or (y > (self.height - 1)):
            return False
        if y in self.maze and x in self.maze.get(y):
            return False
        return True

    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        as_string  = " " + ("_ " * self.width)
        as_string += "\n"

        for y in range(self.height):
            as_string += "|"
            for x in range(self.width):
                cell = self.maze[y][x]
                if cell.get(Direction.SOUTH):
                    as_string += " "
                else:
                    as_string += "_"

                if cell.get(Direction.EAST):
                    as_string += " "
                else:
                    as_string += "|"

            as_string += "\n"

        return as_string
