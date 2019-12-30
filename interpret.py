VERTICES = [0,1,2,3,4]
EDGES = [(0,2),(0,3),(1,3),(2,4),(3,4)]
PATHS = 2
N = len(VERTICES)
D = 2


def inverse_vid(num):
    num -= 1
    if num < PATHS * N**2:
        path = num // N**2
        vertex = (num % N**2) // N
        order = (num % N)
        return path, vertex, order
    else:
        num -= PATHS * N**2
        dtuple = num // PATHS
        path = (num % PATHS)
        return dtuple, path

def text2vars(line):
    variables = []
    line = line.split(" ")[1:]
    for var in line:
        if int(var) > 0:
            variables.append(inverse_vid(int(var)))
    return variables

def process(variables, args):
    lin_vars = [var for var in variables if len(var) == 3]
    dtuple_vars = [var for var in variables if len(var) == 2]

    if args.vars:
        print("(Linearization, Vertex, Order)")
        for lv in lin_vars:
            print(lv)
        print("\n(dtuple, Linearization)")
        for dv in dtuple_vars:
            print(dv)

    if args.linearizations:
        for path in range(PATHS):
            path_vars = [var for var in lin_vars if var[0] == path]
            lin = []
            for i in range(N):
                for pv in path_vars:
                    if pv[2] == i:
                        lin.append(pv[1])
            print("Linearization {}:  {}".format(path + 1, lin))

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description = """A program for interpreting
                                    the variable assigmenments made by glucose""")
    parser.add_argument("result", nargs = "?", default = None)
    parser.add_argument("-l", "--linearizations", help="Show linearizations chosen by glucose",
                        action="store_true")
    parser.add_argument("-v", "--vars", help="Show variables in their original notation",
                        action="store_true")
    args = parser.parse_args()

    if args.result != None:
        with open(args.result, "r") as f:
            assignment = f.readlines()[-1]
            process(text2vars(assignment), args)
    else:
        assignment = sys.stdin.readlines()[-1]
        process(text2vars(assignment), args)
