import random
import heapq
import math


# see https://docs.python.org/3.4/library/random.html#notes-on-reproducibility
def randint(f, t):
    return int(f) + int(random.random() * (t - f + 1))


class RandomMaze:
    def __init__(self, seed, w=70, h=22, barriers=4):
        random.seed(int(seed))
        self.w = w
        self.h = h
        if self.w % 2:
            self.w += 1
        if self.h % 2:
            self.h += 1
        portal_y = self._align_portal(int(self.h / 2))
        self.start = (1, portal_y)  # middle of left wall
        self.end = (self.w - 1, portal_y)  # middle of right wall
        self._gen(barriers)

    def _align_portal(self, coord):
        if not coord % 2:
            if coord == self.h:
                return coord - 1
            else:
                return coord + 1
        else:
            return coord

    def _align_barrier(self, coord):
        if coord % 2:
            if coord == self.w:
                return coord - 1
            else:
                return coord + 1
        else:
            return coord

    def neighbors(self, room):
        res = []
        for x in [room[0] - 2, room[0] + 2]:
            if x > 0 and x < self.w:
                res.append((x, room[1]))
        for y in [room[1] - 2, room[1] + 2]:
            if y > 0 and y < self.h:
                res.append((room[0], y))
        return res

    def door(self, room1, room2):
        xdelta = int((room1[0] - room2[0]) / 2)
        ydelta = int((room1[1] - room2[1]) / 2)
        if abs(xdelta) > 1 or abs(ydelta) > 1:
            raise ValueError("Rooms not adjacent")
        return (room1[0] - xdelta, room1[1] - ydelta)

    def can_walk(self, x, y):
        if self.map[y][x] == " ":
            return True
        else:
            return False

    def _make_door(self, room1, room2):
        x, y = self.door(room1, room2)
        self._excavate(x, y)

    def _excavate(self, x, y):
        row = self.map[y]
        self.map[y] = row[:x] + " " + row[x + 1:]

    def _fill(self, x, y):
        row = self.map[y]
        self.map[y] = row[:x] + "#" + row[x + 1:]

    def _make_vbarrier(self, bx, bsy, bh):
        # build
        for y in range(bsy + 1, bsy + bh, 2):
            self._fill(bx, y)
        # excavate sides
        for y in range(bsy, bsy + bh, 2):
            self._excavate(bx - 1, y)
            self._excavate(bx + 1, y)
        # excavate top and bottom
        self._excavate(bx, bsy - 1)
        self._excavate(bx, bsy + bh)

    def _inigrid(self):
        hwall = "#" * (self.w + 1)
        hcorr = "# " * int(self.w / 2) + "#"
        self.map = [hwall]
        for i in range(int(self.h / 2)):
            self.map.append(hcorr)
            self.map.append(hwall)
        self._excavate(self.start[0] - 1, self.start[1])
        self._excavate(self.end[0] + 1, self.end[1])

    def _make_barriers(self, barriers, barrier_h):
        bh = min(int(self.h * barrier_h), self.h - 3)
        if not bh % 2:
            bh -= 1
        bsy = int((self.h + 1 - bh) / 2)
        if bsy % 2:
            bh -= 2
            bsy += 1
        bxstep = int(self.w / (barriers + 1))
        bx = [self._align_barrier(x)
              for x in range(0, self.w, bxstep)
              if x > 3 and x < self.w - 3]
        for x in bx:
            self._make_vbarrier(x, bsy, bh)

    def _gen(self, barriers, barrier_h=0.7):
        self._inigrid()
        seen = set()
        stack = []
        room_count = int((self.h / 2) * (self.w / 2))
        curr = self.start
        seen.add(curr)
        while len(seen) < room_count:
            children = [child for child in self.neighbors(curr)
                        if child not in seen]
            if children:
                selected = children[randint(0, len(children) - 1)]
                stack.append(curr)  # push
                self._make_door(curr, selected)
                curr = selected
                seen.add(curr)
            else:
                curr = stack.pop()
        self._make_barriers(barriers, barrier_h)

    def dump(self):
        for row in self.map:
            print(row)


class Node:
    def __init__(self, coord, path_cost=0, parent=None, depth=0):
        self.coord = coord
        self.g = path_cost
        self.parent = parent
        self.depth = depth

    def __repr__(self):
        return str(self.coord)

    def __hash__(self):
        return hash(self.coord)

    def __eq__(self, other):
        if self.coord == other.coord:
            return True
        else:
            return False

    def path_cost(self):
        return self.g


class SearchProblem(RandomMaze):
    def start_node(self):
        return Node(self.start)

    def is_goal(self, node):
        return node.coord == self.end

    def expand(self, node):
        children = []
        for room in self.neighbors(node.coord):
            dx, dy = self.door(node.coord, room)
            if self.can_walk(dx, dy):
                children.append(Node(room, node.g + 2, node, node.depth + 1))
        return children

    def print_path(self, node):
        path = [node]
        g = node.path_cost()
        while node.parent is not None:
            path.insert(0, node.parent)
            node = node.parent
        for node in path:
            if self.is_goal(node):
                print("GOAL: ", end="")
            print(node, end=", ")
        print("COST: %d" % (g))

    def print_solution(self, node):
        footprints = set([node.coord])
        while node.parent is not None:
            footprints.add(self.door(node.coord, node.parent.coord))
            footprints.add(node.parent.coord)
            node = node.parent

        print(self.map[0])
        for y in range(1, self.h):
            scanline = []
            for x in range(self.w + 1):
                if (x, y) in footprints:
                    scanline.append(".")
                else:
                    scanline.append(self.map[y][x])
            print("".join(scanline))
        print(self.map[self.h])


class Fringe:
    def __init__(self):
        self._h = []
        self.serial = 0

    def remove_front(self):
        return heapq.heappop(self._h)[2]

    def _add(self, priority, tiebreak, node):
        heapq.heappush(self._h, (priority, tiebreak, node))
        self.serial += 1

    def add_front(self, node):
        self._add(0, -self.serial, node)

    def add_end(self, node):
        self._add(0, self.serial, node)

    def add_by_priority(self, node, priority):
        self._add(priority, self.serial, node)

    def is_empty(self):
        return len(self._h) == 0

    def __iter__(self):
        return (node for priority, tiebreak, node in sorted(self._h))

    def __len__(self):
        return len(self._h)


def h1(problem, node):
    """Manhattan distance"""
    xdelta = problem.end[0] - node.coord[0]
    ydelta = problem.end[1] - node.coord[1]
    return abs(xdelta) + abs(ydelta)


def h2(problem, node):
    """Srtaight-line distance"""
    xdelta = problem.end[0] - node.coord[0]
    ydelta = problem.end[1] - node.coord[1]
    return math.sqrt(ydelta * ydelta + xdelta * xdelta)


def in_path(node, cand):
    if node == cand:
        return True
    while node.parent:
        if node.parent == cand:
            return True
        node = node.parent
    return False
