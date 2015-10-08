__author__ = 'Martin, Kaspar'

import random

from lab2 import SearchProblem, Fringe


def silly_search(problem):
    fringe = Fringe()
    fringe.add_front(problem.start_node())

    while 1:  # lõputu tsükkel
        if fringe.is_empty():
            return None  # ei leitud lahendust

        node = fringe.remove_front()
        if problem.is_goal(node):
            return node  # puu tipp. Tee siit puu juurikasse ongi lahendus

        children = problem.expand(node)  # children on list tyypi; [ node1, node2, .... ]
        fringe.add_front(random.choice(children))  # valime yhe ja paneme jrk ette


p = SearchProblem(131333)
res = silly_search(p)
print("\nLahendamata labürint")
p.dump()
if res is None:
    print("Not found")
else:
    print("\nLahendatud labürint")
    p.print_path(res)
    p.print_solution(res)
