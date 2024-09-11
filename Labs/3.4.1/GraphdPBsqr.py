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

MARKERS = [
    "k.",
    "k^",
    "ko",
    "kv",
    "ks",
    "kx",
]

def main() -> None:
    draw_graphs([
        "dP(Bsqr)CuRise.csv",
        "dP(Bsqr)CuFall.csv",
        ])


def draw_graphs(files: list[str]) -> None:
    fig = plt.figure(figsize=[10, 10])
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_title("dP(B^2)")
    axes.set_xlabel("B^2, Tl^2")
    axes.set_ylabel("dP, μN")
    axes.grid()

    for i, file in enumerate(files):
        if (not check_file(file)):
            return
        draw_graph(axes, file, COLORS[i], MARKERS[i])

    axes.legend()

    fig.savefig("dP(Bsqr)Cu.png")
    fig.show()
    plt.show()


def check_file(file: str) -> bool:
    if file.endswith(".csv"):
        return True
    print("BAD FILE!!!!!!!")
    return False


def draw_graph(axes, file: str, color: str, marker: str):
    Y, X = get_y_x(file)
    Xlinspace = np.linspace(X[0], X[-1], 50)

    axes.plot(X, Y, marker, markersize=10.0)

    def f(x, a, b):
        return a * x + b

    popt, pcov = curve_fit(f, X, Y)

    print(f"{popt}\n{get_stddev(pcov)}")

    line, = axes.plot(Xlinspace, f(Xlinspace, *popt), color=color)
    line.set_label(file.removesuffix(".csv").removeprefix("./"))


def get_y_x(file: str):
    with open(file, 'r') as f:
        reader = pd.read_csv(f)
    Y = np.array(reader["Y"])
    X = np.array(reader["X"])

    return Y, X


def get_stddev(pcov):
    return np.sqrt(np.diag(pcov))


if __name__ == '__main__':
    main()

