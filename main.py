__author__ = 'Martin, Kaspar'

import lab2
from statistics import Statistics

KASPAR_CODE = 131333
MARTIN_CODE = 131316
STEN_CODE = 111

class Search():
    def __init__(self):
        rec_node = None

    #################### A* ###################################
    def A_STAR(problem, stat):
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
                new_cost2 = node.path_cost() + lab2.h1(problem, node)

                if new_cost < closed_list.get(child, float("inf")):
                    closed_list[child] = new_cost
                    priority = new_cost + lab2.h1(problem, child)
                    fringe.add_by_priority(child, priority)

    ################## GREEDY ###############################
    def GREEDY(problem, stat):
        fringe = lab2.Fringe()
        start_node = problem.start_node()
        fringe.add_by_priority(start_node, 0)

        while not fringe.is_empty():
            stat.increment_node_que(len(fringe))
            node = fringe.remove_front()
            stat.increment_node_depth(node.depth)
            stat.increment_node_count()
            if problem.is_goal(node):
                return node

            children = problem.expand(node)
            for child in children:
                new_cost = node.path_cost() + lab2.h1(problem, node)
                if child.path_cost() < new_cost:
                    fringe.add_by_priority(child, new_cost)





    def BFS(problem, stat):
        fringe = lab2.Fringe()
        start_node = problem.start_node()
        fringe.add_end(start_node)
        visited = {}
        visited[start_node] = True

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
                if child not in visited:
                    fringe.add_front(child)
                    visited[child] = True

    ####################### DFS SEARCH 3 SOLUTIONS ########################################### FRINGE!!!!
    def DFS(problem, node, stat, visited=set()):
        # Otsingu täiustused punkt 3
        if problem.is_goal(node):
            print("\nLahendatud labürint 3 - DFS meetodil(Sügavuti otsing)")
            p.print_path(node)
            p.print_solution(node)
            print("Läbitud tippe " + str(stat.get_node_count()))
            print("Hargnemistegur: ", stat.get_avg_node_children_count())
            print("Maksimaalne järjekorra pikkus: ", stat.get_max_que())
            print("Puu maksimaalne sügavus: ", stat.get_max_depth())
            return node

        if visited is None:
            visited = set()

        stat.increment_node_que(len(visited))
        stat.increment_node_depth(node.depth)
        stat.increment_node_count()

        visited.add(node)
        children = problem.expand(node)
        stat.increment_node_children_count(len(children))
        for child in children:
            if child not in visited:
                Search.DFS(problem, child, stat, visited)

    def DFS1(problem, node, stat):
        # Otsingu täiustused punkt 1
        if problem.is_goal(node):
            return node

        stat.increment_node_que(1)
        stat.increment_node_depth(node.depth)
        stat.increment_node_count()

        children = problem.expand(node)
        stat.increment_node_children_count(len(children))
        for child in children:
            Search.DFS(problem, child, stat)


# p = lab2.SearchProblem(MARTIN_CODE)
p = lab2.SearchProblem(KASPAR_CODE)
initial_state = p.start_node()
stat1 = Statistics()
stat2 = Statistics()
stat3 = Statistics()
stat4 = Statistics()
res1 = Search.A_STAR(p, stat1)
res2 = Search.BFS(p, stat2)

Search.DFS(p, p.start_node(), stat3)
# res4 = Search.GREEDY(p, stat4)



# print("\nLahendamata labürint")
#p.dump()
if res1 is None:
    print("Not found")
else:
    print("\nLahendatud labürint 1 - A* meetodil")
    p.print_path(res1)
    p.print_solution(res1)
    print("Läbitud tippe " + str(stat1.get_node_count()))
    print("Hargnemistegur: ", stat1.get_avg_node_children_count())
    print("Maksimaalne järjekorra pikkus: ", stat1.get_max_que())
    print("Puu maksimaalne sügavus: ", stat1.get_max_depth())

    if res2 is not None:
        print("\nLahendatud labürint 2 - BFS meetodil(Laiuti otsing)")
        p.print_path(res2)
        p.print_solution(res2)
        print("Läbitud tippe " + str(stat2.get_node_count()))
        print("Hargnemistegur: ", stat2.get_avg_node_children_count())
        print("Maksimaalne järjekorra pikkus: ", stat2.get_max_que())
        print("Puu maksimaalne sügavus: ", stat2.get_max_depth())

        # if res4 is not None:
        #   print("\nLahendatud labürint 3 - DFS meetodil(Sügavuti otsing)")
        #  p.print_path(v1)
        # p.print_solution(v1)
        # print("Läbitud tippe " + str(stat3.get_node_count()))
        # print("Hargnemistegur: ", stat3.get_avg_node_children_count())
        # print("Maksimaalne järjekorra pikkus: ", stat3.get_max_que())
        # print("Puu maksimaalne sügavus: ", stat3.get_max_depth())
