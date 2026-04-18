class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        return self.frontier.pop()


class Maze:
    def __init__(self, filename):

        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one starting point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == "#":
                        row.append(True)
                    else:
                        row.append(False)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        self.num_explored = 0

    # ---------------- OUTPUT FUNCTION ----------------
    def output(self, show_solution=True):
        solution = self.solution[1] if self.solution and show_solution else None

        lines = []
        for i, row in enumerate(self.walls):
            line = ""
            for j, col in enumerate(row):

                if col:
                    line += "⬛"
                elif (i, j) == self.start:
                    line += "A"
                elif (i, j) == self.goal:
                    line += "B"
                elif solution and (i, j) in solution:
                    line += "*"
                else:
                    line += "⬜"

            lines.append(line)

        return "\n".join(lines)

    # UPDATED PRINT FUNCTION
    def print(self, show_solution=True):
        print(self.output(show_solution))

    def neighbors(self, state):
        row, col = state

        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))

        return result

    def solve(self):

        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        self.explored = set()

        while True:

            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:

                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()

                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


# ---------------- RUN PROGRAM ----------------

if __name__ == "__main__":
    maze = Maze("maze.txt")

    print("\nMaze:\n")
    print(maze.output(show_solution=False))

    print("\nSolving...\n")
    maze.solve()

    print(f"States Explored: {maze.num_explored}\n")

    print("Solution:\n")
    print(maze.output(show_solution=True))