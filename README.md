# lttb-bench

Started as speed comparison of different [lttb](https://github.com/sveinn-steinarsson/flot-downsample) implementations for Python.

Morphed into attempt at cython implementation which seemed to work and was faster than the two python versions, but still way slower than the plain C.

ARGH.

Finally, I found three different mistakes I made in the translation from C which
when fixed, resulted in the cython implementation performing within 10 to 15% of
the C one.

See [the notebook](./drag_race_lttb.ipynb) for more detail, and how to run this.

## Random notes

To get cython 3 installed, I had to:

```shell
poetry add --allow-prereleases cython@latest
```

## Pythran module compilation

The Pythran module `lttb_pt` is compiled with:

```shell
pythran lttb_pt.py
```
