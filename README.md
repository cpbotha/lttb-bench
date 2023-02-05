# lttb-bench

Started as speed comparison of different [lttb](https://github.com/sveinn-steinarsson/flot-downsample) implementations for Python.

Morphed into attempt at cython implementation which seems to work and is faster than the two python versions, but still way slower than the plain C.

ARGH.

See [the notebook](./drag_race_lttb.ipynb) for more detail, and how to run this.

## Random notes

To get cython 3 installed, I had to:

```shell
poetry add --allow-prereleases cython@latest
```
