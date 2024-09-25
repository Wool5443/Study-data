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
    draw_graphs([
        "./U(I)14.csv",
        "./U(I)31.csv",
        "./U(I)48.csv",
        "./U(I)65.csv",
        "./U(I)82.csv",
        "./U(I)99.csv",
        ])


def draw_graphs(files: list[str]) -> None:
    fig = plt.figure(figsize=[10, 10])

    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_title(f"EHall(B)")
    axes.set_xlabel("B, mTl")
    axes.set_ylabel("E Hall, mV")
    axes.grid()

    for i, file in enumerate(files):
        if not check_file(file):
            return
        draw_graph(axes, file, COLORS[i])

    fig.savefig(file.removesuffix(".csv").removeprefix("./") + '.png')
    fig.show()
    plt.show()


def check_file(file: str) -> bool:
    if file.endswith(".csv"):
        return True
    print("BAD FILE!!!!!!!")
    return False


def draw_graph(axes, file: str, color: str):
    Isample, eH, Im = get_e_i(file)
    XImSmooth = np.linspace(Im[0], Im[-1], 50)

    axes.plot(Im, eH, "k^", markersize=10.0)

    def f(x, a, b, c):
        return a * np.square(x) + b * x + c

    popt, pcov = curve_fit(f, Im, eH)

    line, = axes.plot(XImSmooth, f(XImSmooth, *popt), color=color)
    line.set_label(file.removesuffix(".csv").removeprefix("./"))


def get_e_i(file: str):
    with open(file, 'r') as f:
        reader = pd.read_csv(f)

    Isample = reader["Isc, mA"][0]

    Im  = np.array(reader["Im, A"])
    U0  = np.array(reader["U0, mV"])
    U34 = np.array(reader["U34, mV"])
    eH  = U34 - U0

    return Isample, eH, Im


if __name__ == '__main__':
    main()
