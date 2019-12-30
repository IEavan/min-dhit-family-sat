import itertools
from params import *


def vvid(path, vertex, order):
    return path * N**2 + vertex * N + order + 1

def tvid(dtuple, path):
    return PATHS * N**2 + PATHS * dtuple + path + 1

def happens_before():
    clauses = []
    for p in range(PATHS):
        for u,v in EDGES:
            for i in range(N - 1):
                for j in range(i + 1, N):
                    clauses.append([-vvid(p, v, i), -vvid(p, u, j)])
    return clauses

def one_var_per_order():
    clauses = []
    for p in range(PATHS):
        # Encode at least one
        for i in range(N):
            clause = [vvid(p, v, i) for v in VERTICES]
            clauses.append(clause)

        # Encode no pairs (i.e. no more than one)
        for i in range(N):
            for u in range(N):
                for v in range(N):
                    if v == u:
                        continue
                    else:
                        clauses.append([-vvid(p, u, i), -vvid(p, v, i)])

        # Encode vertex used only once
        for i in range(N - 1):
            for j in range(i + 1, N):
                for v in range(N):
                    clauses.append([-vvid(p, v, i), -vvid(p, v, j)])
    return clauses

def gen_d_tuples():
    dtuples = []
    for dtuple in itertools.permutations(VERTICES, D):
        if is_admissable(dtuple):
            dtuples.append(dtuple)
    return dtuples

def is_admissable(dtuple):
    illegal_vertices = []
    for v in dtuple:
        if not v in illegal_vertices:
            add_predecessors(v, illegal_vertices)
        else:
            return False
    return True

def add_predecessors(vertex, illegal_vertices):
    incoming_edges = [edge for edge in EDGES if edge[1] == vertex]
    for edge in incoming_edges:
        if not edge[0] in illegal_vertices:
            illegal_vertices.append(edge[0])
            add_predecessors(edge[0], illegal_vertices)

def must_hit_tuples():
    clauses = []
    for t, dtuple in enumerate(gen_d_tuples()):
        must_hit_t = [tvid(t, p) for p in range(PATHS)]
        clauses.append(must_hit_t)
        for p in range(PATHS):
            start_clause = [vvid(p, dtuple[0], i) for i in range(N - D + 1)]
            start_clause.append(-tvid(t, p))
            clauses.append(start_clause)
            for k in range(D - 1):
                for i in range(k, N - D + k + 1):
                    end_clause = [vvid(p, dtuple[k + 1], j) for j in range(i + 1, N - D + k + 2)]
                    end_clause.append(-vvid(p, dtuple[k], i))
                    end_clause.append(-tvid(t, p))
                    clauses.append(end_clause)
    return clauses

def to_dimacs(clauses):
    result = ""
    for clause in clauses:
        for lit in clause:
            result += str(lit) + " "
        result += "0\n"
    return result

def output_cnf(stream):
    hb = happens_before()
    ovpo = one_var_per_order()
    mht = must_hit_tuples()

    num_clauses = len(hb) + len(ovpo) + len(mht)
    num_vars = tvid(len(gen_d_tuples()) - 1, PATHS - 1)

    stream.write("p cnf " + str(num_vars) + " " + str(num_clauses) + "\n")
    stream.write(to_dimacs(ovpo))
    stream.write(to_dimacs(mht))
    stream.write(to_dimacs(hb))

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Program for generating the CNF-SAT formula")
    parser.add_argument("file", nargs="?", help="Optional file to write output to", default=None)
    args = parser.parse_args()

    if not args.file is None:
        with open(args.file, "w+") as cnf:
            output_cnf(cnf)
    else:
        output_cnf(sys.stdout)
        sys.stdout.close()
