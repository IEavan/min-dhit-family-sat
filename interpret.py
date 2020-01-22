from graphs import SimpleGraph


def inverse_vid(num, linearizations, graph):
    num -= 1
    if num < linearizations * graph.N**2:
        path = num // graph.N**2
        vertex = (num % graph.N**2) // graph.N
        order = (num % graph.N)
        return path, vertex, order
    else:
        num -= linearizations * graph.N**2
        dtuple = num // linearizations
        path = (num % linearizations)
        return dtuple, path


def text2vars(line, linearizations, graph):
    variables = []
    line = line.split(" ")[1:]
    for var in line:
        if int(var) > 0:
            variables.append(inverse_vid(int(var), linearizations, graph))
    return variables


def get_linearizations(lin_vars, linearizations, graph):
    lins = []
    for path in range(linearizations):
        path_vars = [var for var in lin_vars if var[0] == path]
        lin = []
        for i in range(graph.N):
            for pv in path_vars:
                if pv[2] == i:
                    lin.append(pv[1])
        lins.append(lin)
    return lins


def split_vars(variables):
    lin_vars = [var for var in variables if len(var) == 3]
    dtuple_vars = [var for var in variables if len(var) == 2]
    return lin_vars, dtuple_vars


def process(variables, args, graphs):
    lin_vars, dtuple_vars = split_vars(variables)

    if args.vars:
        print("(Linearization, Vertex, Order)")
        for lv in lin_vars:
            print(lv)
        print("\n(dtuple, Linearization)")
        for dv in dtuple_vars:
            print(dv)

    if args.linearizations:
        for i, linearization in enumerate(get_linearizations(lin_vars, args.linearizations, graph)):
            print("Linearization {}:  {}".format(i + 1, linearization))


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="""A program for interpreting
                                    the variable assigmenments made by glucose""")
    parser.add_argument("result", nargs="?", default=None,
                        help="Glucose output with the model flag set")
    parser.add_argument("graph", help="Graph definition file")
    parser.add_argument("-l", "--linearizations", type=int, metavar="L", required=True,
                        help="Show given number of linearizations chosen by glucose")
    parser.add_argument("-v", "--vars", help="Show variables in their original notation",
                        action="store_true")
    args = parser.parse_args()
    graph = SimpleGraph(args.graph)

    if args.result != None:
        with open(args.result, "r") as f:
            assignment = f.readlines()[-1]
    else:
        assignment = sys.stdin.readlines()[-1]

    if assignment == "s UNSATISFIABLE\n":
        print("UNSATISFIABLE")
        sys.exit()
    else:
        print("SATISFIABLE")

    process(text2vars(assignment, args, graph), args)
