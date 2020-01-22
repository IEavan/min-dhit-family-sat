import networkx as nx
from networkx.algorithms import approximation
import matplotlib.pyplot as plt
import sys
import numpy as np


def read_dimacs(stream):
    num_vars, num_clauses = stream.readline().split(" ")[-2:]
    clauses = []
    for clause_line in stream.readlines():
        variables = clause_line.split(" ")
        variables = [int(v) for v in variables if v != "0"]
        clauses.append(variables)
    return clauses


def gen_incidense(cnf):
    graph = nx.Graph()
    for i, clause in enumerate(cnf):
        for var in clause:
            graph.add_edge(abs(var), -(i+1))
    return graph


def view_graph(graph):
    nx.draw(graph)
    plt.show()


def show_hist(graph, bins=100):
    degrees = np.asarray([d for n, d in graph.degree()])
    hist_values, _ = np.histogram(degrees, bins=bins)
    plt.hist(hist_values, bins=bins)
    plt.show()


def show_props(graph):
    print("Nodes: {}, Edges: {}".format(len(graph.nodes), len(graph.edges)))
    treewidth, decomp = approximation.treewidth_min_degree(graph)
    print("TreeWidth: {}".format(treewidth))
    cluster_ceof = approximation.clustering_coefficient.average_clustering(graph)
    print("Average Clustering Coefficient: {}".format(cluster_ceof))
    print("Is Acyclic: {}".format(nx.is_forest(graph)))
    print("Max degree: {}".format(max([d for n, d in graph.degree()])))
    # diameter = nx.algorithms.distance_measures.diameter(graph)
    # print("Diameter: {}".format(diameter))

    # Max clique is not interesting will always be 2
    # print("Max Clique: {}".format(nx.algorithms.clique.graph_clique_number(graph)))

    # Connectivity
    # k = 1
    # while True:
    #     if nx.algorithms.connectivity.is_k_edge_connected(graph, k):
    #         k += 1
    #     else:
    #         break
    # print("{}-edge-connected".format(k))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate, visualize and \
        analyze the incidence graph of the CNF-SAT reduction.")

    parser.add_argument("cnf", nargs="?", default=None,
                        help="Read dimacs cnf file, default to STDIN")
    parser.add_argument("-v", "--view", action="store_true",
                        help="Use networkx and matplotlib viewer")
    parser.add_argument("-d", "--dot", help="Write graph to dot file")
    parser.add_argument("--hist", action="store_true",
                        help="show histogram of node degrees")
    parser.add_argument("-p", "--props", action="store_true",
                        help="show simple properties")
    args = parser.parse_args()

    if args.cnf is None:
        cnf_source = sys.stdin
    else:
        cnf_source = open(args.cnf)
    cnf = read_dimacs(cnf_source)
    incidense = gen_incidense(cnf)

    if args.view:
        view_graph(incidense)
    if args.dot:
        nx.drawing.nx_agraph.write_dot(incidense, args.dot)
    if args.hist:
        show_hist(incidense)
    if args.props:
        show_props(incidense)
