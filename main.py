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

    def a_multiplication(problem, stat, end):
        # lol = Otsi()

        fringe = lab2.Fringe()
        fringe.add_front(problem.start_node())
        visited = set()
        visited.add(problem.start_node())

        nodes_to_visit = set()

        start_node = problem.start_node()
        fringe.add_by_priority(start_node, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start_node] = None
        cost_so_far[start_node] = 0

        while not fringe.is_empty():
            current = fringe.remove_front()

            if problem.is_goal(current):
                return current

            children = problem.expand(current)
            stat.increment_node_que(len(children))

            for next in children:
                stat.increment_node_count()

                new_cost = cost_so_far[current] + next.path_cost() - current.path_cost()
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    # fringe.add_by_priority(next, )
                    priority = new_cost + lab2.h1(problem, next)
                    fringe.add_by_priority(next, priority)
                    came_from[next] = current

            ### STATS ###
            stat.increment_node_children_count(len(children))
            stat.increment_node_depth(current.depth)

        return came_from, cost_so_far




p = lab2.SearchProblem(MARTIN_CODE)
# p = SearchProblem(KASPAR_CODE)
initial_state = p.start_node()
stat = Statistics()
stat2 = Statistics()
stat3 = Statistics()
res = Search.silly_search(p, stat)
res2 = Search.god_damn_search(p, stat2)
res3 = Search.a_multiplication(p, stat3, res2)

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
