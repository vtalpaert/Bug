import sys
import matplotlib.pyplot as plt
import numpy as np


def draw(graphs):
    for k in graphs:
        if type(k) == int:
            plt.figure(k)
            plt.clf()
            plt.grid()
            for l in graphs[k]:
                plt.plot(np.array(range(len(l))), np.array(l))
            plt.ion()
            plt.pause(0.001)
            plt.show(block=False)


if __name__ == "__main__":
    graphs = {}
    for line in sys.stdin:
        try:
            numbers = map(float, line.split())
            if len(numbers) not in graphs.keys():
                graphs[len(numbers)] = [[] for _ in range(len(numbers))]
            for l_index, l in enumerate(graphs[len(numbers)]):
                l.append(numbers[l_index])
            draw(graphs)
        except ValueError:
            sys.stderr.write(line + '(IGNORED)')
