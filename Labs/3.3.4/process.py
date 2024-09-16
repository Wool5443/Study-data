from sys import argv
import numpy as np
import matplotlib.pyplot as plt
import csv

def main() -> None:
    # if len(argv) == 1:
    #     print("No input files, try again!")
    #     return
    # draw_graphs(argv[1:])
    draw_graphs(["./U(I)14.csv"])


def draw_graphs(files: list[str]) -> None:
    for file in files:
        if not check_file(file):
            return
        draw_graph(file)


def check_file(file: str) -> bool:
    if file.endswith(".csv"):
        return True
    print("BAD FILE!!!!!!!")
    return False


def draw_graph(file: str):
    Isample = 0
    U0      = 0

    Imagnet = []
    U34     = []
    eHall   = []
    with open(file, 'r') as f:
        reader = csv.reader(f)

        for i, line in enumerate(reader):
            if i == 0:
                continue
            if i == 1:
                Isample = float(line[0])
                U0      = float(line[1])
            Imagnet.append(float(line[2]))
            U34.append(float(line[3]))
            eHall.append(U34[-1] - U0)

    plt.plot(eHall, Imagnet)

main()
