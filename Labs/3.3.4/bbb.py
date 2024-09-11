import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig = plt.figure()

ax = fig.add_axes([0, 0, 1, 1])

ax.plot(x, y)
ax.set_title("Sinx")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid()
ax.axhline()
ax.axvline()

plt.show()
