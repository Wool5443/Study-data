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

    Iscs   = []
    ks     = []
    ks_dev = []

    for i, file in enumerate(files):
        if not check_file(file):
            return
        I, k, kd = draw_graph(axes, file, COLORS[i], MARKERS[i])
        Iscs.append(I)
        ks.append(k)
        ks_dev.append(kd)

    axes.legend()

    fig.savefig("eHall(B).png")
    fig.show()

    Iscs   = np.array(Iscs)
    ks     = np.array(ks)
    ks_dev = np.array(ks_dev)

    k_table = {
        "$Isc, mA$": Iscs,
        "$K, \\frac{V}{Tl}$": ks,
        "$\\sigma_K, \\frac{V}{Tl}$": ks_dev,
        "$\\varepsilon_K, \\frac{V}{Tl}$": ks_dev / ks,
    }

    df = pd.DataFrame(k_table)
    df.to_csv("K(Isc).csv", index=False)

    plt.show()


def check_file(file: str) -> bool:
    if file.endswith(".csv"):
        return True
    print("BAD FILE!!!!!!!")
    return False


def draw_graph(axes, file: str, color: str, marker: str):
    Isample, eH, B = get_e_b(file)
    XBSmooth = np.linspace(B[0], B[-1], 50)

    axes.plot(B, eH, marker, markersize=10.0)

    def f(x, b, c):
        return b * x + c

    popt, pcov = curve_fit(f, B, eH)

    line, = axes.plot(XBSmooth, f(XBSmooth, *popt), color=color)

    line.set_label(f"Isample = {Isample}mA")

    return Isample, popt[0], get_stddev(pcov)[0]


def get_stddev(pcov):
    return np.sqrt(np.diag(pcov))


def get_b(Im):
    return -362.82003477 * np.square(Im) + 1314.38160385 * Im -70.43240556


def get_e_b(file: str):
    with open(file, 'r') as f:
        reader = pd.read_csv(f)

    Isample = reader["Isc, mA"][0]

    Im  = np.array(reader["Im, A"])
    B   = get_b(Im)
    U0  = np.array(reader["U0, mV"])
    U34 = np.array(reader["U34, mV"])
    eH  = U34 - U0

    return Isample, eH, B


if __name__ == '__main__':
    main()
