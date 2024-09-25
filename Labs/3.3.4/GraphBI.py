import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from   scipy.optimize import curve_fit

FULL_FIGURE_RECT = [0.1, 0.1, 0.8, 0.8]

COLORS = [
    "red",
    "green",
    "blue",
    "black",
    "magenta",
    "aquamarine",
]

def main() -> None:
    draw_graphs(["B(I).csv"])


def draw_graphs(files: list[str]) -> None:
    fig = plt.figure(figsize=[10, 10])

    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_title("B(I)")
    axes.set_xlabel("Im, A")
    axes.set_ylabel("B, mTl")
    axes.grid()

    for i, file in enumerate(files):
        if not check_file(file):
            return
        draw_graph(axes, file, COLORS[i])

    axes.legend()

    fig.savefig("B(I).png")
    fig.show()
    plt.show()


def check_file(file: str) -> bool:
    if file.endswith(".csv"):
        return True
    print("BAD FILE!!!!!!!")
    return False


def draw_graph(axes, file: str, color: str):
    B, I = get_b_i(file)
    XISmooth = np.linspace(I[0], I[-1], 50)

    axes.plot(I, B, "k^", markersize=10.0)

    def f(x, a, b, c):
        return a * np.square(x) + b * x + c

    popt, pcov = curve_fit(f, I, B)

    print(f"{popt}\n{get_stddev(pcov)}")

    line, = axes.plot(XISmooth, f(XISmooth, *popt), color=color)
    line.set_label(file.removesuffix(".csv").removeprefix("./"))


def get_stddev(pcov):
    return np.sqrt(np.diag(pcov))


def get_b_i(file: str):
    with open(file, 'r') as f:
        reader = pd.read_csv(f)

    I  = np.array(reader["I, A"])
    B1 = np.array(reader["B1, mTl"])
    B2 = np.array(reader["B1, mTl"])
    B3 = np.array(reader["B1, mTl"])

    B  = (B1 + B2 + B3) / 3

    return B, I


if __name__ == '__main__':
    main()
