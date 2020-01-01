import sys
from collections import defaultdict

class SimpleGraph():
    def __init__(self, inputfile):
        """ Read in a graph in the trivial graph format """

        self.vertices = []
        self.outgoing_edges = defaultdict(list)
        self.incoming_edges = defaultdict(list)

        if inputfile is sys.stdin:
            graph_definition = sys.stdin.readlines()
        else:
            with open(inputfile, "r") as f:
                graph_definition = f.readlines()

        reading_vertices = True
        for line in graph_definition:
            if line == "#\n":
                reading_vertices = False
                continue

            if reading_vertices:
                new_vertex = line.split(" ")[0]
                self.vertices.append(int(new_vertex))
            else:
                tail_vertex, head_vertex = line.split(" ")[:2]
                self.outgoing_edges[int(tail_vertex)].append(int(head_vertex))
                self.incoming_edges[int(head_vertex)].append(int(tail_vertex))

        self.N = len(self.vertices)
        self.M = sum([len(edges) for edges in self.outgoing_edges.values()])

    def edge_list(self):
        for tail_vertex, adjacent_vertices in self.outgoing_edges.items():
            for head_vertex in adjacent_vertices:
                yield tail_vertex, head_vertex

    def save(self, filename):
        """ Write out the graph in the trivial graph format """

        with open(filename, "w+") as f:
            for vertex in self.vertices:
                f.write("{}\n".format(vertex))
            f.write("#\n")
            for tail_vertex, adjacent_vertices in self.outgoing_edges.items():
                for head_vertex in adjacent_vertices:
                    f.write("{} {}\n".format(head_vertex, tail_vertex))
