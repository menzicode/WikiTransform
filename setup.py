from setuptools import setup
from Cython.Build import cythonize

setup(
    name='WikiTransform',
    ext_modules=cythonize("./WikiTransform/database.py",
                          compiler_directives={'language_level': "3"}),
    zip_safe=False,
)
