import itertools
from graphs import SimpleGraph


def vvid(linearization, vertex, order, graph):
    return linearization * graph.N**2 + vertex * graph.N + order + 1

def tvid(dtuple, linearization, args, graph):
    return args.linearizations * graph.N**2 + \
           args.linearizations * dtuple + linearization + 1

def happens_before(args, graph):
    clauses = []
    for p in range(args.linearizations):
        for u,v in graph.edge_list():
            for i in range(graph.N - 1):
                for j in range(i + 1, graph.N):
                    clauses.append([-vvid(p, v, i, graph), -vvid(p, u, j, graph)])
    return clauses

def one_var_per_order(args, graph):
    clauses = []
    for p in range(args.linearizations):
        # Encode at least one
        for i in range(graph.N):
            clause = [vvid(p, v, i, graph) for v in graph.vertices]
            clauses.append(clause)

        # Encode no pairs (i.e. no more than one)
        for i in range(graph.N):
            for u in range(graph.N):
                for v in range(graph.N):
                    if v == u:
                        continue
                    else:
                        clauses.append([-vvid(p, u, i, graph), -vvid(p, v, i, graph)])

        # Encode vertex used only once
        for i in range(graph.N - 1):
            for j in range(i + 1, graph.N):
                for v in range(graph.N):
                    clauses.append([-vvid(p, v, i, graph), -vvid(p, v, j, graph)])
    return clauses

def gen_d_tuples(args, graph):
    dtuples = []
    for dtuple in itertools.permutations(graph.vertices, args.depth):
        if is_admissable(dtuple, graph):
            dtuples.append(dtuple)
    return dtuples

def is_admissable(dtuple, graph):
    illegal_vertices = []
    for v in dtuple:
        if not v in illegal_vertices:
            add_predecessors(v, illegal_vertices, graph)
        else:
            return False
    return True

def add_predecessors(vertex, illegal_vertices, graph):
    parents = graph.incoming_edges[vertex]
    for parent in parents:
        if not parent in illegal_vertices:
            illegal_vertices.append(parent)
            add_predecessors(parent, illegal_vertices, graph)

def must_hit_tuples(args, graph):
    clauses = []
    for t, dtuple in enumerate(gen_d_tuples(args, graph)):
        must_hit_t = [tvid(t, p, args, graph) for p in range(args.linearizations)]
        clauses.append(must_hit_t)
        for p in range(args.linearizations):
            start_clause = [vvid(p, dtuple[0], i, graph) for i in range(graph.N - args.depth + 1)]
            start_clause.append(-tvid(t, p, args, graph))
            clauses.append(start_clause)
            for k in range(args.depth - 1):
                for i in range(k, graph.N - args.depth + k + 1):
                    end_clause = [vvid(p, dtuple[k + 1], j, graph) for j in range(i + 1, graph.N - args.depth + k + 2)]
                    end_clause.append(-vvid(p, dtuple[k], i, graph))
                    end_clause.append(-tvid(t, p, args, graph))
                    clauses.append(end_clause)
    return clauses

def to_dimacs(clauses):
    result = ""
    for clause in clauses:
        for lit in clause:
            result += str(lit) + " "
        result += "0\n"
    return result

def output_cnf(stream, args, graph):
    hb = happens_before(args, graph)
    ovpo = one_var_per_order(args, graph)
    mht = must_hit_tuples(args, graph)

    num_clauses = len(hb) + len(ovpo) + len(mht)
    num_vars = tvid(len(gen_d_tuples(args, graph)) - 1, args.linearizations - 1, args, graph)

    stream.write("p cnf " + str(num_vars) + " " + str(num_clauses) + "\n")
    stream.write(to_dimacs(ovpo))
    stream.write(to_dimacs(mht))
    stream.write(to_dimacs(hb))

if __name__ == "__main__":
    import sys
    import argparse

    # Read arguments
    parser = argparse.ArgumentParser(
            description="Program for generating the CNF-SAT formula from a graph")
    parser.add_argument("graph", nargs="?", default=sys.stdin,
            help="Graph definition file to read from, defaults to STDIN")
    parser.add_argument("output_file", nargs="?",
            help="Optional file to write output to", default=None)
    parser.add_argument("-d", "--depth", default=2, type=int, metavar="D",
            help="Depth of bugs that the linearizations must discover")
    parser.add_argument("-l", "--linearizations", default=2, type=int, metavar="L",
            help="Number of linearizations that are allowed")
    args = parser.parse_args()

    # Construct Graph
    graph = SimpleGraph(args.graph)

    if not args.output_file is None:
        with open(args.output_file, "w+") as cnf:
            output_cnf(cnf, args, graph)
    else:
        output_cnf(sys.stdout, args, graph)
        sys.stdout.close()
