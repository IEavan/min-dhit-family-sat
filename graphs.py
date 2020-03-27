import sys
import random
from collections import defaultdict

class SimpleGraph():
    def __init__(self, inputfile=None):
        """ Read in a graph in the trivial graph format """

        self.vertices = []
        self.outgoing_edges = defaultdict(list)
        self.incoming_edges = defaultdict(list)

        # Read graph data if it exists
        if not inputfile is None:
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
                    if not int(tail_vertex) in self.vertices or not int(head_vertex) in self.vertices:
                        raise ValueError("Edge ({}, {}) contains undefined vertices".format(tail_vertex, head_vertex))
                    self.outgoing_edges[int(tail_vertex)].append(int(head_vertex))
                    self.incoming_edges[int(head_vertex)].append(int(tail_vertex))

        self.N = len(self.vertices)
        self.M = sum([len(edges) for edges in self.outgoing_edges.values()])

    def edge_list(self):
        for tail_vertex, adjacent_vertices in self.outgoing_edges.items():
            for head_vertex in adjacent_vertices:
                yield tail_vertex, head_vertex

    def add_vertices(self, new_vertices):
        for vertex in new_vertices:
            if vertex not in self.vertices:
                self.vertices.append(vertex)
                self.N += 1

    def add_edges(self, new_edges):
        for edge in new_edges:
            head_vertex, tail_vertex = edge
            if not tail_vertex in self.vertices or not head_vertex in self.vertices:
                raise ValueError("Edge ({}, {}) contains undefined vertices".format(tail_vertex, head_vertex))

            if not head_vertex in self.outgoing_edges[tail_vertex]:
                self.outgoing_edges[tail_vertex].append(head_vertex)
                self.incoming_edges[head_vertex].append(tail_vertex)
                self.M += 1

    def to_tgf_string(self):
        result = ""
        for vertex in self.vertices:
            result += "{}\n".format(vertex)
        result += "#\n"
        for tail_vertex, adjacent_vertices in self.outgoing_edges.items():
            for head_vertex in adjacent_vertices:
                result += "{} {}\n".format(head_vertex, tail_vertex)

        return result


    def save(self, filename):
        """ Write out the graph in the trivial graph format """

        with open(filename, "w+") as f:
            f.write(self.to_tgf_string())


def random_dag(num_vertices, edge_probability=0.5):
    dag = SimpleGraph()
    dag.add_vertices(list(range(num_vertices)))

    edges = []
    for i in range(num_vertices - 1):
        for j in range(i+1, num_vertices):
            if random.random() < edge_probability:
                edges.append((i,j))

    dag.add_edges(edges)
    return dag

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, help="Type of graph to generate")
    parser.add_argument("-n", "--nodes", type=int, help="Number of nodes")

    args = parser.parse_args()
    
    if args.type == "chains":
        graph = SimpleGraph()
        chain_length = args.nodes // 2
        for chain in [0,1]:
            vertices = list(range(chain * chain_length, (chain + 1) * chain_length))
            graph.add_vertices(vertices)
            graph.add_edges(zip(vertices[:-1],vertices[1:]))

    sys.stdout.write(graph.to_tgf_string())
    sys.stdout.flush()
