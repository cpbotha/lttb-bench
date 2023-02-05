# python setup.py build_ext --inplace
from setuptools import Extension, setup
from Cython.Build import cythonize


extensions = [
    # only with Cython 3 and up, define NPY_* to avoid the OLD API
    # https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#configuring-the-c-build    
    Extension("lttbcy", ["lttbcy.pyx"], define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])
]

setup(
    ext_modules = cythonize(extensions)
)
