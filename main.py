__author__ = 'Martin, Kaspar'

import random
import lab2

from statistics import Statistics

KASPAR_CODE = 131333
MARTIN_CODE = 131316
STEN_CODE = 111

class Search():
    def silly_search(problem, stat):
        fringe = lab2.Fringe()
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
            stat.increment_node_depth(node.depth)
            stat.increment_node_children_count(len(children))


    def god_damn_search(problem, stat):
        fringe = lab2.Fringe()
        fringe.add_front(problem.start_node())
        visited = set()
        visited.add(problem.start_node())

        while 1:  # lõputu tsükkel
            # Solution missing for the maze
            if fringe.is_empty():
                return None
            node = fringe.remove_front()

            # Solution found
            if problem.is_goal(node):
                return node

            children = problem.expand(node) # children on list tyypi; [ node1, node2, .... ]
            for child in children:
                # Deal with statistics here
                stat.increment_node_count()

                if child not in visited:
                    fringe.add_end(child)  # valime yhe ja paneme jrk ette
                    visited.add(child)

            stat.increment_node_children_count(len(children))
            stat.increment_node_depth(node.depth)





p = lab2.SearchProblem(MARTIN_CODE)
# p = SearchProblem(KASPAR_CODE)
initial_state = p.start_node()
stat = Statistics()
stat2 = Statistics()
res = Search.silly_search(p, stat)
res2 = Search.god_damn_search(p, stat2)
print("\nLahendamata labürint")
p.dump()
if res is None:
    print("Not found")
else:
    print("\nLahendatud labürint 1")
    p.print_path(res)
    p.print_solution(res)
    print("Läbitud tippe " + str(stat.get_node_count()))
    print("Hargnemistegur: ", stat.get_avg_node_children_count())
    print("Maksimaalne järjekorra pikkus: valmimisel")
    print("Puu maksimaalne sügavus: ", stat.get_max_depth())

    if res2 is not None:
        print("\nLahendatud labürint 1")
        p.print_path(res2)
        p.print_solution(res2)
        print("Läbitud tippe " + str(stat2.get_node_count()))
        print("Hargnemistegur: ", stat2.get_avg_node_children_count())
        print("Maksimaalne järjekorra pikkus: valmimisel")
        print("Puu maksimaalne sügavus: ", stat2.get_max_depth())
