import matplotlib as plt
import numpy as np
import pandas as pd

FF_1 = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "B"], index=["a", "b"])  # pyright: ignore[reportArgumentType]


print(FF_1.values)
