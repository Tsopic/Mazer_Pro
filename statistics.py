__author__ = 'kaspar'


class Statistics:
    def __init__(self):
        self.node_count = 0

    def increment_node_count(self):
        self.node_count += 1

    def get_node_count(self):
        return self.node_count
