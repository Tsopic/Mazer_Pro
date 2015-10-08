__author__ = 'Martin, Kaspar'

import random

from lab2 import SearchProblem, Fringe
from statistics import Statistics

KASPAR_CODE = 131333
MARTIN_CODE = 666
STEN_CODE = 111


def silly_search(problem, stat):
    fringe = Fringe()
    fringe.add_front(problem.start_node())

    while 1:  # lõputu tsükkel
        # Solution missing for the maze
        if fringe.is_empty():
            return None

        node = fringe.remove_front()

        # Solution found
        if problem.is_goal(node):
            return node

        children = problem.expand(node)  # children on list tyypi; [ node1, node2, .... ]
        fringe.add_front(random.choice(children))  # valime yhe ja paneme jrk ette

        # Deal with statistics here
        stat.increment_node_count()


p = SearchProblem(KASPAR_CODE)
stat = Statistics()
res = silly_search(p, stat)
print("\nLahendamata labürint")
p.dump()
if res is None:
    print("Not found")
else:
    print("\nLahendatud labürint")
    p.print_path(res)
    p.print_solution(res)
    print("Läbitud tippe " + str(stat.get_node_count()))
