import sys
import matplotlib.pyplot as plt

filename = sys.argv[1]
with open(filename, 'r') as f:
    lines = f.readlines()
x_data = []
y_data = []
for line in lines:
    x, y = map(float, line.split())
    x_data.append(x)
    y_data.append(y)

plt.plot(x_data, y_data)
plt.xlabel('t')
plt.ylabel('T')

plt.show()

