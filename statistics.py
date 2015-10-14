__author__ = 'kaspar'


class Statistics:
    def __init__(self):
        self.node_count = 0
        self.node_depth = 0
        self.node_children = {}

    # ================== NODE TOTAL COUNT ==================
    def increment_node_count(self):
        self.node_count += 1

    def get_node_count(self):
        return self.node_count

    # ================== NODE AVG CHILDREN ==================
    def increment_node_children_count(self, children_count):
        self.node_children[self.node_count] = children_count

    def get_avg_node_children_count(self):
        total = 0
        for k, v in self.node_children.items():
            total += v

        return total / self.node_count

    # ================== Node max depth ==================
    def increment_node_depth(self, depth):
        if depth > self.node_depth:
            self.node_depth = depth

    def get_max_depth(self):
        return self.node_depth
