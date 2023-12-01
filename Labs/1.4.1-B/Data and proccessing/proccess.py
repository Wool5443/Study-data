import numpy as np
from matplotlib import pyplot as plt
from math import pi

def calc_g(J_0, m_g, y, T, M, x_c):
    return 4 * pi ** 2 * (J_0 + m_g * y ** 2) / (T ** 2 * M * x_c)

def main():
    CM_TO_M = 0.01
    GR_TO_KG = 0.001
    with open('data.txt') as f:
        l_rod = float(f.readline().strip()) * CM_TO_M
        x_c0  = float(f.readline().strip()) * CM_TO_M
        z     = float(f.readline().strip()) * CM_TO_M
        m_pr  = float(f.readline().strip()) * GR_TO_KG
        m_rod = float(f.readline().strip()) * GR_TO_KG
        m_gr  = float(f.readline().strip()) * GR_TO_KG

        x_c0  = z - x_c0

        N     = int(f.readline().strip())

        ts    = np.array([0.0] * N)
        ns    = np.array([0.0] * N)
        x_cs  = np.array([0.0] * N)

        for i in range(N):
            ts[i], ns[i], x_cs[i] = map(float, f.readline().strip().split())
        x_cs *= CM_TO_M

    J_0 = m_rod * l_rod ** 2 / 12 + m_rod * x_c0 ** 2
    ys  = ((m_rod + m_pr + m_gr) * x_cs - (m_rod + m_pr) * x_c0) / m_gr

    Ts = ts / ns

    for i in range(N):
        print(f'{ts[i]:0.2f} & {ns[i]} & {Ts[i]:0.4f} & {ys[i] * 100:0.4f} & {calc_g(J_0, m_gr, ys[i], Ts[i], m_rod + m_pr + m_gr, x_cs[i]):0.4f} \\\\')
    
    u = Ts ** 2 * x_cs
    v = ys ** 2

    plt.scatter(ys, Ts)
    plt.plot(ys, Ts)

    k = 1
    c = 0.3905

    u2 = v * k + c

    g = 4 * pi ** 2 * m_gr / (m_rod + m_gr + m_pr)

    print(g)

#    plt.plot(v, u2, color='r')

    plt.savefig('graph2.png', dpi=300)


main()

