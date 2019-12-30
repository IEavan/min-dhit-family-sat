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


if __name__ == "__main__":
    with open("result", "r") as f:
        assignment = f.readlines()[-1]
        assignment = assignment.split(" ")[1:]
        for var in assignment:
            if int(var) > 0:
                print(inverse_vid(int(var)))
