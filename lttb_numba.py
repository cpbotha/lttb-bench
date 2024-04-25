"""Downsample data using the Largest-Triangle-Three-Buckets algorithm.

Tweaked for numba from https://git.sr.ht/~javiljoen/lttb-numpy
which is Copyright (c) 2020, JA Viljoen, MIT license.

Reference
---------
Sveinn Steinarsson. 2013. Downsampling Time Series for Visual
Representation. MSc thesis. University of Iceland.
"""

from numba import jit
import numpy as np


@jit(nopython=True)
def _areas_of_triangles(a, bs, c):
    bs_minus_a = bs - a
    a_minus_bs = a - bs
    # numba could not do built-in abs
    return 0.5 * np.abs(
        (a[0] - c[0]) * (bs_minus_a[:, 1]) - (a_minus_bs[:, 0]) * (c[1] - a[1])
    )


# numba does not support "axis" argument so we have this workaround
# https://github.com/numba/numba/issues/1269#issuecomment-1629763092
@jit(nopython=True)
def numba_mean(x, axis=None):
    if axis is None:
        return np.sum(x, axis) / np.prod(x.shape)
    else:
        return np.sum(x, axis) / x.shape[axis]


@jit(nopython=True)
def numba_downsample(data, n_out):
    if n_out > data.shape[0]:
        raise ValueError("n_out must be <= number of rows in data")

    if n_out == data.shape[0]:
        return data

    if n_out < 3:
        raise ValueError("Can only downsample to a minimum of 3 points")

    # Split data into bins
    n_bins = n_out - 2
    data_bins = np.array_split(data[1 : len(data) - 1], n_bins)

    # Prepare output array
    # First and last points are the same as in the input.
    out = np.zeros((n_out, 2))
    out[0] = data[0]
    out[-1] = data[-1]

    # c = np.empty(2)

    # Largest Triangle Three Buckets (LTTB):
    # In each bin, find the point that makes the largest triangle
    # with the point saved in the previous bin
    # and the centroid of the points in the next bin.
    for i in range(len(data_bins)):
        this_bin = data_bins[i]

        if i < n_bins - 1:
            next_bin = data_bins[i + 1]
        else:
            next_bin = data[-1:]

        a = out[i]
        bs = this_bin
        # numba does not support arguments to np.mean DURN
        # https://stackoverflow.com/a/64314661/532513
        # next_bin.mean(axis=0, out=c)
        c = numba_mean(next_bin, axis=0)

        areas = _areas_of_triangles(a, bs, c)
        out[i + 1] = bs[np.argmax(areas)]

    return out
