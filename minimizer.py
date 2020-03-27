import sys
import graphs
import gen_cnf
import interpret
import io
import subprocess

GLUCOSE = "/home/eavan/Downloads/old/glucose-syrup-4.1/parallel/glucose-syrup_static"


def exp_search(graph, depth):
    linearizations = 1
    while True:
        print("Testing L = {}".format(linearizations))
        sat, min_lins = run(graph, linearizations, depth)
        if sat:
            print("Upper Bound = {}".format(linearizations))
            break
        else:
            linearizations *= 2

    lower_bound = int(linearizations / 2)
    upper_bound = linearizations
    while lower_bound != upper_bound - 1:
        middle = int((lower_bound + upper_bound) / 2)
        print("Testing L = {}".format(middle))
        sat, lins = run(graph, middle, depth)

        if sat:
            upper_bound = middle
            min_lins = lins
        else:
            lower_bound = middle

        print("Range: {} -- {}".format(lower_bound, upper_bound))

    return min_lins


def run(graph, linearizations, depth):
    """ Run reduction through glucose and interpret """

    # Collect reduction into a stream
    with io.StringIO() as reduction:
        gen_cnf.output_cnf(reduction, linearizations, depth, graph)
        cnf = reduction.getvalue()

    proc = subprocess.Popen([GLUCOSE, "-model"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    sat_result = proc.communicate(cnf.encode("utf-8"))[0].decode("utf-8")
    assignment = sat_result.splitlines()[-1]

    if assignment == "s UNSATISFIABLE":
        return False, None
    else:
        variables = interpret.text2vars(assignment, linearizations, graph)
        lin_vars, dtuple_vars = interpret.split_vars(variables)
        lins = interpret.get_linearizations(lin_vars, linearizations, graph)
        return True, lins


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph_file", default=sys.stdin, help="Graph definition file")
    parser.add_argument("-d", "--depth", type=int, metavar="D", required=True,
                        help="Given bug depth to test")

    args = parser.parse_args()
    graph = graphs.SimpleGraph(args.graph_file)
    D = args.depth

    lins = exp_search(graph, D)

    print("\nMinimum {}-hitting familiy of size {}:".format(D, len(lins)))
    print(lins)
