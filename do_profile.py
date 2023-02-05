# i could not get this to spit out line profiling stats

import pstats, cProfile
import pandas as pd
import timeit


import lttbcy

df = pd.read_csv("timeseries.csv")
tseries = df.values
x = tseries[:,0]
y = tseries[:,1]
THRESHOLD = 250


#lttbcy.downsample(x,y,THRESHOLD)

def time_lttbcy():
    # extremely sucky -- this just spits out a number, no mention of the units anywhere
    print(timeit.timeit(lambda: lttbcy.downsample(x,y,THRESHOLD), number=1_000))

#time_lttbcy()

cProfile.runctx("time_lttbcy()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()

