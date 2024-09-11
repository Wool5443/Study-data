import matplotlib.pyplot as plot
from math import factorial as fact
from math import exp

# TODO scipy.optimize.curve_fit


class Data_Tau:
    _counter = 0
    def __init__(self, data: list, tau: int):
        self.id: int = type(self)._counter
        type(self)._counter += 1

        self.data: list[int] = data
        self.tau: int = tau
        self.data_tau: list[int] = self.calculate_data_tau()

        self.average: float = self.calculate_average()
        self.dispersion: float = self.calculate_dispersion()
        self.error_rate: float = self.calculate_error_rate()

        self.counts_table: dict[int, int] = self.calculate_counts()
        self.frequencies_table: dict[int, float] = self.calculate_frequencies()

        self.sigma_inclusions = self.calculate_sigma_inclusions()


    def calculate_data_tau(self) -> list[int]:
        prefs = [0] * (len(self.data) + 1)
        prefs[1] = self.data[0]

        for i in range(2, len(prefs)):
            prefs[i] = prefs[i - 1] + self.data[i - 1]

        data_tau = [0] * (len(self.data) // self.tau)

        for i in range(len(data_tau)):
            data_tau[i] = prefs[(i + 1) * self.tau] - prefs[i * self.tau]

        return data_tau


    def calculate_counts(self) -> dict[int, int]:
        counts_table: dict = {}
        for el in self.data_tau:
            if el in counts_table:
                counts_table[el] += 1
            else:
                counts_table[el] = 1
        return counts_table


    def calculate_frequencies(self) -> dict[int, float]:
        frequencies_table = {}

        for el in self.counts_table:
            frequencies_table[el] = self.counts_table[el] / len(self.data_tau)
        
        return frequencies_table


    def calculate_average(self) -> float:
        return sum(self.data_tau) / len(self.data_tau)


    def calculate_dispersion(self) -> float:
        dispersion_sq = 0
        for el in self.data_tau:
            dispersion_sq += (el - self.average) ** 2
        
        return (dispersion_sq / len(self.data_tau)) ** 0.5


    def calculate_error_rate(self) -> float:
        return self.dispersion / (len(self.data_tau) ** 0.5)
    

    def calculate_sigma_inclusions(self) -> list[float]:
        sigma_inclusions = [0, 0, 0]

        for el in self.data_tau:
            t = abs(el - self.average)
            if t < self.dispersion:
                sigma_inclusions[0] += 1
            if t < self.dispersion * 2:
                sigma_inclusions[1] += 1
            if t < self.dispersion * 3:
                sigma_inclusions[2] += 1
        
        sigma_inclusions[0] /= len(self.data_tau)
        sigma_inclusions[1] /= len(self.data_tau)
        sigma_inclusions[2] /= len(self.data_tau)

        return sigma_inclusions


    def plot_frequencies_table(self, x_lim, colors):
        points = sorted(self.frequencies_table.items())

        ANNOTATION_HEIGHT = 0.01

        x = []
        y = []
        for el in points:
            if el[0] <= x_lim:
                x.append(el[0])
                y.append(el[1]) 

        plot.bar(x, y, width=1, color=colors[self.id % len(colors)])
        plot.annotate(f'tau = {self.tau}s', xy=(40, 0.13 - ANNOTATION_HEIGHT * self.id), color=colors[self.id % len(colors)])

        # plot.savefig(f'Figure {self.tau}.png', dpi=300)
        # plot.close()


def main():
    path = 'Python/data good.txt'
    data = read_file(path)

    taus = [10, 20, 30]
    colors = 'bgrcmykw'
    x_lim = 50

    plot.xlabel('Number of particles')
    plot.ylabel('Frequency')

    for tau in taus:
        print(f'tau = {tau}')
        data_tau = Data_Tau(data, tau)

        with open(f'{path} tau = {tau}.txt', 'w') as f:
            print(f'Number of measures = {len(data_tau.data_tau)}',
                  f'Average particles = {data_tau.average}',
                  f'Dispersion = {data_tau.dispersion}',
                  f'Sigma inclusions = {data_tau.sigma_inclusions}',
                  f'Error rate = {data_tau.error_rate}',
                  f'Average intensity = {data_tau.average / data_tau.tau}',
                  f'Average intensity error = {data_tau.error_rate / data_tau.tau}',
                  file=f, sep='\n')
            
        data_tau.plot_frequencies_table(x_lim, colors)

    data_tau = Data_Tau(data, taus[1])
    data_tau.id -= 1

    X_OFFSET = 0
    xs = [i for i in range(x_lim + X_OFFSET + 1)]
    ys = [0] * len(xs)

    for i, x in enumerate(xs):
        ys[i] = data_tau.average ** x * exp(-data_tau.average) / fact(x)

    plot.plot([max(0, x - X_OFFSET) for x in xs], ys, color=colors[(data_tau.id + 1) % len(colors)])

    plot.savefig('Figure good.png', dpi=300)
    


def read_file(path) -> list:
    with open(path) as f:
        data = [int(x) for x in f.readlines() if x[0] != '#']
    return data


if __name__ == '__main__':
    main()
