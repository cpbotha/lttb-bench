from timeit import timeit
import sys

import lttbc
import lttb
import pylttb

import pyximport
pyximport.install()
import lttbcy

import pandas as pd
import numpy as np

import lttb_pt

# Compile Pythran code, if necessary
if not hasattr(lttb_pt, '__pythran__'):
    print('Please compile `lttb_pt.py` using:')
    print()
    print('  pythran lttb_pt.py')
    print()
    sys.exit(1)


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
