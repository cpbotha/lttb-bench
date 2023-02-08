from timeit import timeit

import lttbc
import lttb
import pylttb

import pyximport
pyximport.install()
import lttbcy
import lttb_pt

import pandas as pd
import numpy as np


N = 100
THRESHOLD = 250


df = pd.read_csv('timeseries.csv')
tseries = np.copy(np.tile(df.values, [100, 1]))

x = np.copy(tseries[:,0])
y = np.copy(tseries[:,1])


print(f"Timeseries length: {len(x)}")
print(f"Reps: 5x{N}")
print()


def clock(name, statement, setup=[], N=N):
    timeit_setup = "\n".join(setup)
    t = timeit(statement, timeit_setup, number=N, globals=globals())
    print(f'{name}: {t:.2f}s')


clock(
    "lttbc",
    "lttbc.downsample(x, y, THRESHOLD)",
    ["import lttbc"]
)

# clock(
#     "lttbc-numpy",
#     "lttb.downsample(tseries, n_out=THRESHOLD, validators=[])"
# )

# clock(
#     "pylttb",
#     "pylttb.lttb(x, y, THRESHOLD)"
# )

clock(
    "lttb-cython",
    "lttbcy.downsample(x, y, THRESHOLD)",
)

clock(
    "lttb-pythran",
    "lttb_pt.downsample(tseries, THRESHOLD)",
    ["import lttbc"]
)
