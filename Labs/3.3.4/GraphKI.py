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
        "./K(Isc).csv",
        ])


def draw_graphs(files: list[str]) -> None:
    fig = plt.figure(figsize=[10, 10])

    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_title(f"K(Isc)")
    axes.set_xlabel("Isc, mA")
    axes.set_ylabel("K, V/Tl")
    axes.grid()

    for i, file in enumerate(files):
        if not check_file(file):
            return
        draw_graph(axes, file, COLORS[i], MARKERS[i])

    axes.legend()

    fig.savefig("K(Isc).png")
    fig.show()

    plt.show()


def check_file(file: str) -> bool:
    if file.endswith(".csv"):
        return True
    print("BAD FILE!!!!!!!")
    return False


def draw_graph(axes, file: str, color: str, marker: str):
    Isc, K = get_i_k(file)
    XIscSmooth = np.linspace(Isc[0], Isc[-1], 50)

    axes.plot(Isc, K, marker, markersize=10.0)

    def f(x, b, c):
        return b * x + c

    popt, pcov = curve_fit(f, Isc, K)

    print(popt[0], get_stddev(pcov)[0])

    line, = axes.plot(XIscSmooth, f(XIscSmooth, *popt), color=color)

    line.set_label("K(Isc)")


def get_stddev(pcov):
    return np.sqrt(np.diag(pcov))


def get_b(Im):
    return -362.82003477 * np.square(Im) + 1314.38160385 * Im -70.43240556


def get_i_k(file: str):
    with open(file, 'r') as f:
        reader = pd.read_csv(f)

    Isc = reader["$Isc, mA$"]
    K   = reader["$K, \\frac{V}{Tl}$"]

    return np.array(Isc), np.array(K)


if __name__ == '__main__':
    main()
