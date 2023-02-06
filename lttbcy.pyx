# cython: language_level=3

# ported from C https://github.com/dgoeries/lttbc/ to Cython by Charl P. Botha
# to build: python setup.py build_ext --inplace

import numpy as np
import cython
from cpython cimport array
from libc.math cimport floor, fabs

dtype = np.double

# double aka float64
#ctypedef fused double:
#    double

# http://docs.cython.org/en/latest/src/userguide/memoryviews.html
# https://stackoverflow.com/questions/19537673/slow-division-in-cython
@cython.boundscheck(False)
@cython.wraparound(False)
# disable divide-by-zero checks (only needed at one point) -- does not make a big difference
@cython.cdivision(True)
#@cython.profile(True)
def downsample(double[::1] x, double[::1] y, int threshold = 250):
    cdef Py_ssize_t inp_len = x.shape[0]

    # else:
    #     raise RuntimeError("only support double")

    # equally long vectors
    #assert x.shape[0] == y.shape[0], "vectors should be same length"
    # x.shape is an N-tuple, even when I pass 1D vectors
    # instead we test that x[0] and y[0] are floats
    #assert type(x[0]) is float and type(y[0]) is float

    # allocate output with same type as input
    _x_out = np.zeros((threshold,), dtype=dtype)
    #cdef _x_out = array.array("d")
    #array.resize(_x_out, threshold)
    cdef double[::1] x_out = _x_out

    # allocate output with same type as input
    _y_out = np.zeros((threshold,), dtype=dtype)
    #cdef _y_out = array.array("d")
    #array.resize(_y_out, threshold)
    cdef double[::1] y_out = _y_out

    cdef Py_ssize_t out_idx = 0
    # should be const
    cdef double every = (inp_len - 2) / float(threshold - 2)

    cdef Py_ssize_t a = 0;
    cdef Py_ssize_t next_a = 0;

    cdef double max_area_point_x = 0.0;
    cdef double max_area_point_y = 0.0;

    # Always add the first point!
    # we don't have the npy_isfinite() check here
    x_out[out_idx] = x[0]
    y_out[out_idx] = y[0]
    out_idx += 1

    cdef double tmp
    cdef double avg_x
    cdef double avg_y
    cdef int i
    cdef Py_ssize_t avg_range_start
    cdef Py_ssize_t avg_range_end
    cdef Py_ssize_t avg_range_length
    cdef Py_ssize_t range_offs
    cdef Py_ssize_t range_to
    cdef double area
    cdef double max_area
    cdef double xa, xdist
    cdef double ya, ydist

    for i in range(threshold - 2):
        avg_x = 0
        avg_y = 0
        avg_range_start = <Py_ssize_t>(floor((i + 1) * every) + 1)
        avg_range_end = <Py_ssize_t>(floor((i + 2) * every) + 1)

        if avg_range_end >= inp_len:
            avg_range_end = inp_len

        avg_range_length = avg_range_end - avg_range_start

        # for (;avg_range_start < avg_range_end; avg_range_start++){ ...
        while avg_range_start < avg_range_end:
            avg_x += x[avg_range_start]
            avg_y += y[avg_range_start]
            avg_range_start += 1

        # TODO: losing perf here because Py is checking for divide by 0
        avg_x /= avg_range_length
        avg_y /= avg_range_length

        # Get the range for this bucket
        range_offs = <Py_ssize_t>(floor((i + 0) * every) + 1)
        range_to = <Py_ssize_t>(floor((i + 1) * every) + 1)

        max_area = -1.0
        # bringing out these temp variables for fewer lookups in the area = fabs(...) made almost no diff
        xa = x[a]
        ya = y[a]
        xdist = (xa - avg_x)
        ydist = (avg_y - ya)
        while range_offs < range_to:
            # Calculate triangle area over three buckets
            # TODO: we can drop the 0.5 -- will still choose the greatest area correctly
            area = fabs(xdist * (y[range_offs] - ya) - (xa - x[range_offs]) * ydist) * 0.5
            if area > max_area:
                max_area = area
                max_area_point_x = x[range_offs]
                max_area_point_y = y[range_offs]
                next_a = range_offs

            range_offs += 1

        # the point that gave us max area is the one that is picked from this bucket
        x_out[out_idx] = max_area_point_x
        y_out[out_idx] = max_area_point_y

        # go to next bucket
        out_idx += 1
        a = next_a;

    # and we add the last point (but here we don't do npy_isfinite())
    x_out[out_idx] = x[inp_len-1]
    y_out[out_idx] = y[inp_len-1]

    # we were working with the views, but we return the nparray
    return _x_out, _y_out