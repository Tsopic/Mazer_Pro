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
            stat.increment_node_que(len(children))
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
            stat.increment_node_que(len(children))
            for child in children:
                # Deal with statistics here
                stat.increment_node_count()

                if child not in visited:
                    fringe.add_end(child)  # valime yhe ja paneme jrk ette
                    visited.add(child)

            stat.increment_node_children_count(len(children))
            stat.increment_node_depth(node.depth)

    def a_star(problem, stat):
        fringe = lab2.Fringe()

        start_node = problem.start_node()
        fringe.add_by_priority(start_node, 0)
        closed_list = {}
        closed_list[start_node] = 0

        while not fringe.is_empty():
            stat.increment_node_que(len(fringe))
            node = fringe.remove_front()
            stat.increment_node_depth(node.depth)
            stat.increment_node_count()

            if problem.is_goal(node):
                return node

            children = problem.expand(node)
            stat.increment_node_children_count(len(children))

            for child in children:

                new_cost = closed_list[node] + lab2.h1(problem, node)

                if new_cost < closed_list.get(child, float("inf")):
                    closed_list[child] = new_cost
                    priority = new_cost + lab2.h1(problem, child)
                    fringe.add_by_priority(child, priority)

# p = lab2.SearchProblem(MARTIN_CODE)
p = lab2.SearchProblem(KASPAR_CODE)
initial_state = p.start_node()
stat = Statistics()
stat2 = Statistics()
stat3 = Statistics()
res = Search.silly_search(p, stat)
res2 = Search.god_damn_search(p, stat2)
res3 = Search.a_star(p, stat3)

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
    print("Maksimaalne järjekorra pikkus: ", stat.get_max_que())
    print("Puu maksimaalne sügavus: ", stat.get_max_depth())

    if res2 is not None:
        print("\nLahendatud labürint 2")
        p.print_path(res2)
        p.print_solution(res2)
        print("Läbitud tippe " + str(stat2.get_node_count()))
        print("Hargnemistegur: ", stat2.get_avg_node_children_count())
        print("Maksimaalne järjekorra pikkus: ", stat2.get_max_que())
        print("Puu maksimaalne sügavus: ", stat2.get_max_depth())

    if res3 is not None:
        print("\nLahendatud labürint 3 - A* meetodil")
        p.print_path(res3)
        p.print_solution(res3)
        print("Läbitud tippe " + str(stat3.get_node_count()))
        print("Hargnemistegur: ", stat3.get_avg_node_children_count())
        print("Maksimaalne järjekorra pikkus: ", stat3.get_max_que())
        print("Puu maksimaalne sügavus: ", stat3.get_max_depth())
