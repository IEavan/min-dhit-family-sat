VERTICES = [0,1,2,3,4]
EDGES = [(0,2),(0,3),(1,3),(2,4),(3,4)]
PATHS = 2
N = len(VERTICES)
D = 2

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
    #TODO figure out how to get all d-tuples
    return [(0,1),(0,2),(0,3),(0,4),(1,0),(1,2),(1,3),(1,4),(2,1),(2,3),(2,4),(3,2),(3,4)]

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


if __name__ == "__main__":
    with open("reduction.cnf", "w+") as cnf:
        hb = happens_before()
        ovpo = one_var_per_order()
        mht = must_hit_tuples()

        num_clauses = len(hb) + len(ovpo) + len(mht)
        num_vars = tvid(len(gen_d_tuples()) - 1, PATHS - 1)

        cnf.write("p cnf " + str(num_vars) + " " + str(num_clauses) + "\n")
        cnf.write(to_dimacs(ovpo))
        cnf.write(to_dimacs(mht))
        cnf.write(to_dimacs(hb))
