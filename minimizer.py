import graphs
import gen_cnf
import interpret
import subprocess


def exp_search(graph, depth):
    linearizations = 1
    while True:
        sat, _ = run(graph, linearizations, depth)
        if sat:
            break
        else:
            linearizations *= 2

    lower_bound = linearizations / 2
    upper_bound = linearizations
    while lower_bound != upper_bound - 1:
        middle = (lower_bound + upper_bound) // 2
        sat, lins = run(graph, middle, depth)
        
        if sat:
            upper_bound = middle
        else:
            lower_bound = middle

    return lins

def run(graph, linearizations, depth):
    """ Run reduction through glucose and interpret """
    pass

if __name__ == "__main__":
    graph = graphs.SimpleGraph("example_graph.tgf")
    D = 3

    exp_search(graph, D)
